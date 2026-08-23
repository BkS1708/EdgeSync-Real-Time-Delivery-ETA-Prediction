# EdgeSync Research Dossier: Ablation Study Design

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `09_ABLATION_STUDY_DESIGN.md`

---

## 1. Purpose of Ablation Studies

Ablation studies systematically isolate and remove individual system components to measure their specific contribution to overall system performance, decision latency, state consistency, and prediction stability.

---

## 2. Master Ablation Matrix

| Ablation Study | Component Removed | Independent Variable | Dependent Variables | Hypothesis & Expected Research Insight |
| :--- | :--- | :--- | :--- | :--- |
| **Ablation 1** | Geographic Partitioning (`config.get_region`) | Spatial routing logic | Request latency, node load balance | Removing spatial boundaries increases cross-node network hops and degrades spatial locality benefits. |
| **Ablation 2** | Cross-Region Delegation (`/calc_delivery`) | Peer HTTP delegation | Inter-region request completion rate, latency | Removing delegation forces source nodes to compute remote region legs using local data, saving network calls but risking inaccurate local speeds. |
| **Ablation 3** | Gossip Synchronization (`/sync` & daemon) | Gossip thread execution | Inter-node state variance ($\sigma^2_{\text{state}}$) | Disabling gossip causes regional nodes to operate in complete isolation, leading to high state divergence across nodes. |
| **Ablation 4** | Sample-Weighted Averaging | Sample count weighting ($N_{\text{samples}}$) | Convergence rate, noise sensitivity | Replacing sample-weighted averaging with simple unweighted moving average increases sensitivity to outlier ETA requests. |
| **Ablation 5** | Dynamic Traffic Speed Model | Traffic speed mapping (35/25/15 km/h) | ETA prediction accuracy, variance | Replacing dynamic traffic with constant 25 km/h speed underpredicts peak hour ETAs by up to 40%. |
| **Ablation 6** | Stochastic Food Prep Time | Noise multiplier `random.uniform(0.9, 1.1)` | ETA standard deviation | Removing prep noise produces static deterministic prep times, hiding realistic variance in food delivery simulations. |
| **Ablation 7** | Rider Proximity Model | Rider pickup time calculation | Total ETA value, pickup ratio | Omitting rider pickup time ($\text{ETA} = \text{prep} + \text{delivery}$) underestimates total ETA by 10-25%. |

---

## 3. Detailed Experimental Procedures

### Ablation 1 Procedure (Removing Geographic Partitioning)
1. Modify `config.py` to return `"EAST"` unconditionally for all coordinates.
2. Send 1,000 requests distributed across Mumbai coordinates.
3. Compare processing time and network hop count against default EdgeSync.

### Ablation 3 Procedure (Removing Gossip Synchronization)
1. Comment out `threading.Thread(target=gossip, daemon=True).start()` in `east.py`, `west.py`, `central.py`.
2. Issue 500 requests to `EAST` node (High traffic) and 500 requests to `WEST` node (Low traffic).
3. Record `avg_eta` on all 3 nodes every 10 seconds.
4. Plot node state divergence over time to prove gossip maintains state alignment.
