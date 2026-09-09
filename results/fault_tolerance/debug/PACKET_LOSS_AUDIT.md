# EdgeSync Fault-Tolerance — Packet Loss Measurement Audit

**Audit Date/Time:** `2026-08-25 18:00:00`  
**Focus:** Packet loss injection mechanisms, transport emulation, failure trapping, and metric definitions.

---

## 1. Distinct Network Phenomenon & Metric Definitions

To avoid conflation in distributed systems research, we distinguish the following five distinct metrics:

1. **Configured Loss Rate ($\text{loss\_rate}$):** The theoretical probability $p \in \{0.01, 0.05, 0.10\}$ of dropping an inter-service RPC packet.
2. **Injected RPC Drops ($\text{Dropped RPCs}$):** The number of simulated network communication failures induced by `NetworkEmulator.inject_custom_delay()` on remote delegations (`dest_region != region`).
3. **Fallback Activations ($\text{Fallback Triggers}$):** The number of times the microservice caught an inter-service communication failure and executed local fallback estimation.
4. **Application Request Availability ($\text{Availability \%}$):** The proportion of client requests returning HTTP 200 with valid ETA values ($\frac{\text{Success}}{\text{Total}} \times 100$).
5. **Observed Loss Rate ($\text{Observed Loss \%}$):** The measured empirical drop frequency across remote requests:
   $$\text{Observed Loss \%} = \frac{\text{Fallback Triggers on Remote Requests}}{\text{Total Remote Requests}} \times 100$$

---

## 2. Code-Level Investigation of the Packet Loss Pipeline

### 2.1 Where Loss is Injected
In `experiments/network/network_emulator.py`:
```python
def inject_custom_delay(self, latency_ms: float, jitter_ms: float = 0.0, loss_rate: float = 0.0):
    if loss_rate > 0 and random.random() < loss_rate:
        raise ConnectionError(f"Simulated network packet drop (loss={loss_rate})")
    # ... delay injection ...
```

### 2.2 How Nodes Handle Injected Loss
In `east.py`, `west.py`, `central.py` inside `custom_eta`:
```python
try:
    if net_delay_ms > 0 or loss_rate > 0:
        global_emulator.inject_custom_delay(net_delay_ms, loss_rate=loss_rate)

    res = http_session.post(target_url, json={...}, timeout=config.GOSSIP_TIMEOUT).json()
    delivery = res["delivery_time"]
    fallback_used = False
except Exception as e:
    # Fallback local delivery calculation on peer network failure
    delivery = estimate_time_from_distance(
        distance(source, dest),
        traffic_level if dynamic_speed_on else "Medium"
    )
    fallback_used = True
```

### 2.3 Why All 9 Trials Returned HTTP 500 with 0% Observed Loss
In the raw CSV files for `scenario_4_loss_1pct`, `5pct`, `10pct`:
1. `east.py` crashed at line 120 (`dest_region = get_region(dest)`) due to the `TypeError` before the request ever reached the `dest_region != region` delegation branch.
2. Because the request crashed at ingress:
   - `global_emulator.inject_custom_delay` was **never called**.
   - Zero packets were dropped by the emulator.
   - `fallback_triggered` remained `False`.
   - The response status code was HTTP 500.
3. When `packet_loss_statistics.csv` calculated:
   ```python
   fb_rem = sum(1 for r in sc_subset if r["fallback_triggered"])
   obs_loss_pct = round((fb_rem / max(1, tot_rem)) * 100.0, 2)
   ```
   `fb_rem` was `0`, producing `observed_loss_pct = 0.0%`.

---

## 3. Findings & Conclusions

1. The underlying design of `NetworkEmulator.inject_custom_delay(loss_rate=...)` combined with `try...except` local fallback is conceptually sound.
2. In the flawed test execution, the packet loss mechanism was never reached because all requests failed prematurely due to the `get_region` signature bug.
3. Once the `get_region` bug is resolved across all nodes, remote requests will route into the delegation block, stochastic drops will trigger local fallback, and observed loss will match the configured 1%, 5%, and 10% rates within normal binomial sampling variance.
