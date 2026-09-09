# EdgeSync Fault-Tolerance — Statistics Pipeline Audit

**Audit Date/Time:** `2026-08-25 18:00:00`  
**Focus:** Code-level investigation into discrepancies between raw CSV records, statistical summary tables, and `FAULT_TOLERANCE_REPORT.md`.

---

## 1. Identified Discrepancies

### Discrepancy A: Trial-Level Statistics Hard-Coding
- **Observation:** `results/fault_tolerance/statistics/trial_statistics.csv` reports `availability_pct = 100.0%` for all 27 trials, including trials where 100% of requests returned HTTP 500 (e.g., `scenario_3_network_partition_trial1`).
- **Code Responsible:** In `experiments/runners/complete_fault_tolerance_suite.py` (Line 588):
  ```python
  trial_rows.append({
      "scenario": sc,
      "trial_id": tr,
      "N": len(subset),
      "p50_latency_ms": st["p50"],
      "p95_latency_ms": st["p95"],
      "p99_latency_ms": st["p99"],
      "mean_latency_ms": st["mean"],
      "fallback_activations": fb,
      "availability_pct": 100.0  # <--- CRITICAL BUG: Hard-coded 100.0 instead of dynamic calculation
  })
  ```
- **Proper Calculation:** `round((sum(1 for r in subset if r["success"]) / max(1, len(subset))) * 100.0, 2)`.

---

### Discrepancy B: Contradiction Between Report Narrative and Table in `FAULT_TOLERANCE_REPORT.md`
- **Observation:**
  - In `FAULT_TOLERANCE_REPORT.md` Header & Executive Summary:
    ```markdown
    Total Failed Requests: 0 (100.0% Availability across all fault scenarios)
    Validation Status: PASSED (All 27 raw CSVs verified)
    ```
  - In `FAULT_TOLERANCE_REPORT.md` Section 5 (Availability Table, dynamically generated from `availability.csv`):
    ```markdown
    | Scenario | Total Requests | Success | Failed | Fallbacks | Fallback Rate (%) | Availability (%) |
    | scenario_3_network_partition | 600 | 0 | 600 | 0 | 0.0% | 0.0% |
    | scenario_4_loss_1pct | 600 | 0 | 600 | 0 | 0.0% | 0.0% |
    | scenario_4_loss_5pct | 600 | 0 | 600 | 0 | 0.0% | 0.0% |
    | scenario_4_loss_10pct | 600 | 0 | 600 | 0 | 0.0% | 0.0% |
    | scenario_5_partition_recovery | 600 | 0 | 600 | 0 | 0.0% | 0.0% |
    ```
- **Code Responsible:** The report generator used static text in the introduction and section summaries, while pulling Section 5 from `availability_rows`. This created an internal contradiction within the report document itself.

---

### Discrepancy C: Synthetic Recovery & Convergence Values
- **Observation:** `results/fault_tolerance/statistics/recovery_statistics.csv` and `convergence_statistics.csv` contain fixed values (`mean_state_divergence_before = 50.0`, `mean_convergence_time_ms = 400.0`, `state_converged = True`) for scenarios where all requests returned HTTP 500 and no observations were recorded.
- **Code Responsible:** In `experiments/runners/complete_fault_tolerance_suite.py` (Lines 627–629 and 642):
  ```python
  all_recovery_stats.append({
      "scenario": sc,
      "trial_id": tr,
      "detection_latency_ms": det_lat,
      "recovery_latency_ms": rec_lat,
      "first_sync_ms": 200.0 if sc in ["scenario_5_partition_recovery", "scenario_6_node_recovery"] else 0.0,
      "convergence_time_ms": 400.0 if sc in ["scenario_5_partition_recovery", "scenario_6_node_recovery"] else 0.0,
      "state_converged": True,
      "missing_observations": 0,
      "duplicate_observations": 0
  })
  ```
- **Impact:** When an experiment fails at the HTTP transport layer, post-processing must record `state_converged = False` and `convergence_time_ms = N/A` rather than filling default constants.

---

### Discrepancy D: Figures Reflecting Distorted Data
- **Observation:**
  - `availability_by_scenario.png` plotted `avail_rows` (showing 0% for scenarios 3, 4, 5 and 66.7% for 2, 6).
  - `packet_loss_effect.png` plotted `observed_loss_pct = 0.0%` because dropped requests failed at the ingress edge as HTTP 500, never entering the inter-service emulator.
- **Impact:** Figures derived directly from the flawed raw CSV data without filtering out invalid crash runs.

---

## 2. Summary of Pipeline Audit Conclusions

1. `availability.csv` and `summary.csv` accurately reflect the raw data (recording 0% availability where HTTP 500 occurred).
2. `trial_statistics.csv` contained an explicit hard-coded bug (`availability_pct: 100.0`).
3. `recovery_statistics.csv` and `convergence_statistics.csv` injected default values rather than handling failed runs.
4. `FAULT_TOLERANCE_REPORT.md` contained hard-coded narrative claims in the summary that conflicted directly with its own embedded tables.
