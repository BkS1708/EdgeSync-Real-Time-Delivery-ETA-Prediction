# EdgeSync Fault-Tolerance — Convergence Calculation Audit

**Audit Date/Time:** `2026-08-25 18:00:00`  
**Focus:** Convergence measurement algorithms, state hash tracking, and empty-set false positive conditions.

---

## 1. Convergence Definition in EdgeSync

In the EdgeSync architecture, convergence across distributed regional nodes (`EAST`, `WEST`, `CENTRAL`) is defined mathematically as:

$$\text{State}(EAST) \equiv \text{State}(WEST) \equiv \text{State}(CENTRAL)$$

Where:
1. $\text{ObservationIDs}(EAST) = \text{ObservationIDs}(WEST) = \text{ObservationIDs}(CENTRAL)$.
2. $|\text{ObservationIDs}(EAST)| = |\text{ObservationIDs}(WEST)| = |\text{ObservationIDs}(CENTRAL)| > 0$.
3. $\text{SHA-256}(\text{SortedIDs}(EAST)) = \text{SHA-256}(\text{SortedIDs}(WEST)) = \text{SHA-256}(\text{SortedIDs}(CENTRAL))$.
4. $\text{SymmetricDifference}(\text{IDs}_A, \text{IDs}_B) = 0$ for all node pairs $(A, B)$.

---

## 2. Code-Level Investigation of Convergence Calculation

### 2.1 The Live Polling Logic
In `experiments/runners/run_fault_tolerance_experiment.py` (lines 354–375):
```python
while (time.time() - poll_start) < max_poll_sec:
    st_e = get_node_state("EAST")
    st_w = get_node_state("WEST")
    st_c = get_node_state("CENTRAL")

    ids_e = set(st_e["observation_ids"])
    ids_w = set(st_w["observation_ids"])
    ids_c = set(st_c["observation_ids"])

    if len(ids_w) > 0 and first_sync_time is None:
        first_sync_time = round((time.time() - poll_start) * 1000.0, 2)

    if ids_e == ids_w == ids_c and len(ids_e) > 0:
        full_conv_time = round((time.time() - poll_start) * 1000.0, 2)
        converged = True
        break
    time.sleep(0.2)
```

### 2.2 Identification of the Empty-Set Bug in Post-Processing
When an experiment failed due to HTTP 500 errors (as in `scenario_3`, `scenario_4`, `scenario_5`):
1. **Zero Observations Injected:** Because `custom_eta` crashed at line 120, `obs_store.add_observation()` was never executed on EAST.
2. **Empty Store State:** `st_e["observation_ids"] = []`, `st_w["observation_ids"] = []`, `st_c["observation_ids"] = []`.
3. **Symmetric Difference on Empty Sets:**
   $$\text{set}([]) \oplus \text{set}([]) = \emptyset \implies \text{len} = 0$$
   The divergence calculation `len(set(ids_e).symmetric_difference(set(ids_w)))` returned `0`!
4. **Post-Processing Hard-Coding:** In `complete_fault_tolerance_suite.py`, because the post-processor re-read CSVs where requests failed, it defaulted to:
   ```python
   "mean_state_divergence_before": 50.0 if "partition" in sc or "node_recovery" in sc else 0.0,
   "mean_state_divergence_after": 0.0,
   "mean_convergence_time_ms": 400.0,
   "full_convergence_achieved": True
   ```
   This caused the summary table to report that convergence succeeded on 50 observations, even though 0 observations existed!

---

## 3. Required Fixes for Convergence Logic

1. **Precondition Guard:** Convergence must only be evaluated if total valid observations generated during the trial $> 0$.
2. **Explicit Non-Convergence Flag:** If total successful requests $= 0$ or no observations were recorded, record:
   - `state_converged = False`
   - `convergence_time_ms = None` (or `"N/A"`)
   - `mean_state_divergence_before = 0`
   - `mean_state_divergence_after = 0`
3. **Eliminate Hard-Coded Defaults:** All metrics must be computed strictly from real observation snapshots returned by `/state`.
