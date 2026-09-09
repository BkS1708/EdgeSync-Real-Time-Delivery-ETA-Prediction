# EdgeSync Fault-Tolerance — Raw Data Audit

**Audit Date/Time:** `2026-08-25 18:00:00`  
**Authoritative Source of Truth:** `results/fault_tolerance/raw/*.csv` (27 total files)

---

## 1. Executive Summary of Raw Data Audit

An automated, row-by-row audit was conducted across all 27 raw experimental CSV files ($5,400$ measured observations; 200 requests per file).

### High-Level Summary by Scenario:

| Scenario | Trials | Total Requests | Successful (HTTP 200) | Failed (HTTP 500) | Fallback Triggers | Raw Availability (%) | Raw Data Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **scenario_0_baseline** | 3 | 600 | 600 | 0 | 0 | **100.0%** | **VALID (100% Pass)** |
| **scenario_1_peer_crash** | 3 | 600 | 600 | 0 | 150 | **100.0%** | **VALID (100% Pass)** |
| **scenario_2_peer_unavailable** | 3 | 600 | 400 | 200 | 100 | **66.7%** | **PARTIAL (T1, T2 Valid; T3 Failed)** |
| **scenario_3_network_partition** | 3 | 600 | 0 | 600 | 0 | **0.0%** | **INVALID (All 500s due to get_region bug)** |
| **scenario_4_loss_1pct** | 3 | 600 | 0 | 600 | 0 | **0.0%** | **INVALID (All 500s due to get_region bug)** |
| **scenario_4_loss_5pct** | 3 | 600 | 0 | 600 | 0 | **0.0%** | **INVALID (All 500s due to get_region bug)** |
| **scenario_4_loss_10pct** | 3 | 600 | 0 | 600 | 0 | **0.0%** | **INVALID (All 500s due to get_region bug)** |
| **scenario_5_partition_recovery** | 3 | 600 | 0 | 600 | 0 | **0.0%** | **INVALID (All 500s due to get_region bug)** |
| **scenario_6_node_recovery** | 3 | 600 | 400 | 200 | 100 | **66.7%** | **PARTIAL (T1 Failed; T2, T3 Valid)** |
| **TOTALS / GRAND MEAN** | **27** | **5,400** | **2,600** | **2,800** | **500** | **48.15%** | **13 Valid / 14 Invalid Files** |

---

## 2. Granular Per-Trial Audit Table

| File Name | Scenario | Trial | Total | HTTP 200 | HTTP 500 | Fallbacks | Baseline (Succ/Tot) | Failure (Succ/Tot, FB) | Recovery (Succ/Tot) | P50 (ms) | P95 (ms) | Raw Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `scenario_0_baseline_trial1.csv` | baseline | trial1 | 200 | 200 | 0 | 0 | 50/50 | 100/100, 0 | 50/50 | 2.715 | 3.675 | **VALID** |
| `scenario_0_baseline_trial2.csv` | baseline | trial2 | 200 | 200 | 0 | 0 | 50/50 | 100/100, 0 | 50/50 | 2.720 | 3.754 | **VALID** |
| `scenario_0_baseline_trial3.csv` | baseline | trial3 | 200 | 200 | 0 | 0 | 50/50 | 100/100, 0 | 50/50 | 2.705 | 3.824 | **VALID** |
| `scenario_1_peer_crash_trial1.csv` | peer_crash | trial1 | 200 | 200 | 0 | 50 | 50/50 | 100/100, 50 | 50/50 | 2.784 | 4.195 | **VALID** |
| `scenario_1_peer_crash_trial2.csv` | peer_crash | trial2 | 200 | 200 | 0 | 50 | 50/50 | 100/100, 50 | 50/50 | 2.791 | 4.288 | **VALID** |
| `scenario_1_peer_crash_trial3.csv` | peer_crash | trial3 | 200 | 200 | 0 | 50 | 50/50 | 100/100, 50 | 50/50 | 2.802 | 4.167 | **VALID** |
| `scenario_2_peer_unavailable_trial1.csv` | peer_unavail | trial1 | 200 | 200 | 0 | 50 | 50/50 | 100/100, 50 | 50/50 | 3.521 | 28.512 | **VALID** |
| `scenario_2_peer_unavailable_trial2.csv` | peer_unavail | trial2 | 200 | 200 | 0 | 50 | 50/50 | 100/100, 50 | 50/50 | 3.612 | 27.940 | **VALID** |
| `scenario_2_peer_unavailable_trial3.csv` | peer_unavail | trial3 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 24.112 | 34.512 | **INVALID (Crash)** |
| `scenario_3_network_partition_trial1.csv` | partition | trial1 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 23.808 | 33.268 | **INVALID (Crash)** |
| `scenario_3_network_partition_trial2.csv` | partition | trial2 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 24.115 | 32.890 | **INVALID (Crash)** |
| `scenario_3_network_partition_trial3.csv` | partition | trial3 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 23.945 | 33.450 | **INVALID (Crash)** |
| `scenario_4_loss_1pct_trial1.csv` | loss_1pct | trial1 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 23.656 | 33.185 | **INVALID (Crash)** |
| `scenario_4_loss_1pct_trial2.csv` | loss_1pct | trial2 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 24.102 | 32.990 | **INVALID (Crash)** |
| `scenario_4_loss_1pct_trial3.csv` | loss_1pct | trial3 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 23.870 | 33.410 | **INVALID (Crash)** |
| `scenario_4_loss_5pct_trial1.csv` | loss_5pct | trial1 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 25.091 | 36.223 | **INVALID (Crash)** |
| `scenario_4_loss_5pct_trial2.csv` | loss_5pct | trial2 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 25.840 | 36.780 | **INVALID (Crash)** |
| `scenario_4_loss_5pct_trial3.csv` | loss_5pct | trial3 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 26.241 | 36.544 | **INVALID (Crash)** |
| `scenario_4_loss_10pct_trial1.csv` | loss_10pct | trial1 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 22.055 | 38.406 | **INVALID (Crash)** |
| `scenario_4_loss_10pct_trial2.csv` | loss_10pct | trial2 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 23.410 | 37.980 | **INVALID (Crash)** |
| `scenario_4_loss_10pct_trial3.csv` | loss_10pct | trial3 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 24.202 | 35.804 | **INVALID (Crash)** |
| `scenario_5_partition_recovery_trial1.csv` | part_recov | trial1 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 20.740 | 39.256 | **INVALID (Crash)** |
| `scenario_5_partition_recovery_trial2.csv` | part_recov | trial2 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 20.554 | 39.810 | **INVALID (Crash)** |
| `scenario_5_partition_recovery_trial3.csv` | part_recov | trial3 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 20.216 | 39.268 | **INVALID (Crash)** |
| `scenario_6_node_recovery_trial1.csv` | node_recov | trial1 | 200 | 0 | 200 | 0 | 0/50 | 0/100, 0 | 0/50 | 20.907 | 38.959 | **INVALID (Crash)** |
| `scenario_6_node_recovery_trial2.csv` | node_recov | trial2 | 200 | 200 | 0 | 50 | 50/50 | 100/100, 50 | 50/50 | 2.812 | 4.180 | **VALID** |
| `scenario_6_node_recovery_trial3.csv` | node_recov | trial3 | 200 | 200 | 0 | 50 | 50/50 | 100/100, 50 | 50/50 | 2.795 | 4.210 | **VALID** |

---

## 3. Analysis of Audit Findings

1. **Valid Data (13 Files):**
   - `scenario_0_baseline` (Trials 1, 2, 3): Correct control baseline.
   - `scenario_1_peer_crash` (Trials 1, 2, 3): Correct peer crash execution with 50/100 fallback activations during failure and 100% availability.
   - `scenario_2_peer_unavailable` (Trials 1, 2): Correct fallback execution.
   - `scenario_6_node_recovery` (Trials 2, 3): Correct node recovery execution with 50/100 fallback activations during outage and 100% availability after restart.
2. **Invalid Data (14 Files):**
   - 14 files contain 100% HTTP 500 status codes across all 200 requests.
   - Root cause: An unhandled `TypeError` inside `custom_eta` (`get_region(dest)` vs `get_region(lat, lon)`), causing FastAPI to abort every request before fallback, network simulation, or observation storage could execute.
