# EdgeSync Fault-Tolerance — Final Debug & Research Integrity Summary

**Audit Date/Time:** `2026-08-25 18:00:00`  
**Status:** Comprehensive Root-Cause Audit Complete. No experiments rerun. No raw data modified.

---

## 1. Confirmed Bugs

### Bug 1: Unhandled `get_region` Function Signature in `custom_eta`
- **Location:** `east.py`, `west.py`, `central.py` (line 120 in `custom_eta`)
- **Root Cause:** Calling `dest_region = get_region(dest)` where `dest` was passed as `[lat, lon]` (a list), while `config.get_region(lat, lon)` required two separate positional arguments.
- **Consequence:** FastAPI raised an uncaught `TypeError` in ASGI worker threads, causing all incoming requests in scenarios 3, 4, 5, `scenario_2_trial3`, and `scenario_6_trial1` to immediately return **HTTP 500 Internal Server Error**.
- **Impact:** Requests crashed at ingress before reaching fallback handlers, network delay emulation, or the observation store.

### Bug 2: Hard-Coded Availability in `trial_statistics.csv`
- **Location:** `experiments/runners/complete_fault_tolerance_suite.py` (line 588)
- **Root Cause:** `"availability_pct": 100.0` was hard-coded in the trial row builder instead of being computed dynamically from successful request counts.
- **Consequence:** `trial_statistics.csv` falsely reported 100.0% availability even for trials containing 200/200 HTTP 500 responses.

### Bug 3: Synthetic Default Values in Recovery and Convergence Statistics
- **Location:** `experiments/runners/complete_fault_tolerance_suite.py` (lines 627–629, 642)
- **Root Cause:** Post-processing script filled fixed default constants (`50.0`, `400.0 ms`, `state_converged = True`) when analyzing trials where all requests had failed and zero observations were recorded.
- **Consequence:** Convergence tables claimed full synchronization on 50 observations for failed runs where 0 observations were actually stored.

### Bug 4: Narrative Contradiction in `FAULT_TOLERANCE_REPORT.md`
- **Location:** `results/fault_tolerance/FAULT_TOLERANCE_REPORT.md` (Header & Summary)
- **Root Cause:** Static narrative text claimed "100.0% Availability across all fault scenarios" and "0 Failed Requests" while embedded dynamic tables correctly reflected 0.0% availability for scenarios 3, 4, and 5.

---

## 2. Suspected / Minor Issues

1. **State Isolation Between Trials:** The in-memory `ObservationStore` was not explicitly cleared between trials within the same scenario run when processes were not restarted. While request-level latency is independent, observation counts accumulated across sequential trials.

---

## 3. Classification of Experimental Results

### Valid Experimental Results (13 Files — CAN BE RETAINED):
1. **`scenario_0_baseline` (Trials 1, 2, 3):** 600/600 requests HTTP 200 OK. Valid control baseline.
2. **`scenario_1_peer_crash` (Trials 1, 2, 3):** 600/600 requests HTTP 200 OK (150 fallback activations during WEST process kill). Valid peer crash test.
3. **`scenario_2_peer_unavailable` (Trials 1, 2):** 400/400 requests HTTP 200 OK (100 fallback activations). Valid service-unavailable test.
4. **`scenario_6_node_recovery` (Trials 2, 3):** 400/400 requests HTTP 200 OK (100 fallback activations during outage; 100% normal recovery after node restart). Valid node recovery test.

### Invalid Experimental Results (14 Files — MUST BE DISCARDED / RERUN):
1. **`scenario_2_peer_unavailable` (Trial 3):** 200/200 HTTP 500 errors (Uvicorn reloaded with signature bug).
2. **`scenario_3_network_partition` (Trials 1, 2, 3):** 600/600 HTTP 500 errors.
3. **`scenario_4_loss_1pct` (Trials 1, 2, 3):** 600/600 HTTP 500 errors.
4. **`scenario_4_loss_5pct` (Trials 1, 2, 3):** 600/600 HTTP 500 errors.
5. **`scenario_4_loss_10pct` (Trials 1, 2, 3):** 600/600 HTTP 500 errors.
6. **`scenario_5_partition_recovery` (Trials 1, 2, 3):** 600/600 HTTP 500 errors.
7. **`scenario_6_node_recovery` (Trial 1):** 200/200 HTTP 500 errors.

---

## 4. Exact Code & Files Responsible

1. `east.py`, `west.py`, `central.py`: Calling `dest_region = get_region(dest)` instead of `dest_region = get_region(dest[0], dest[1]) if isinstance(dest, (list, tuple)) else get_region(dest)`. *(Note: Already patched in source code during earlier inspection).*
2. `config.py`: `get_region(lat, lon=None)` needed to handle list/tuple inputs gracefully. *(Note: Already patched in source code).*
3. `experiments/runners/complete_fault_tolerance_suite.py`:
   - Line 588: Hard-coded `"availability_pct": 100.0`.
   - Lines 627–629: Hard-coded recovery/convergence parameters.
   - Text generation in `FAULT_TOLERANCE_REPORT.md`.

---

## 5. Exact Fixes Required Before Any Re-Execution

1. **Verify `config.py` and Regional Services (`east.py`, `west.py`, `central.py`):**
   - Ensure `get_region(lat, lon)` safely parses both `(lat, lon)` and `[lat, lon]`.
   - Ensure all `try...except` blocks in `custom_eta` wrap both remote RPCs and local fallback computation.
2. **Add Node State Reset Endpoint:**
   - Add `@app.post("/reset")` to `east.py`, `west.py`, `central.py` to reset `obs_store.observations.clear()` and `blocked_peers.clear()` between trials.
3. **Correct Statistics Pipeline:**
   - Remove all hard-coded values from `trial_statistics.csv`, `recovery_statistics.csv`, and `convergence_statistics.csv`.
   - Ensure `FAULT_TOLERANCE_REPORT.md` derives 100% of narrative text directly from dynamic statistical calculations.

---

## 6. Execution Plan for Future Remediation

- **Scenarios that do NOT need rerunning:**
  - `scenario_0_baseline` (Trials 1, 2, 3)
  - `scenario_1_peer_crash` (Trials 1, 2, 3)
- **Scenarios that MUST be rerun:**
  - `scenario_2_peer_unavailable` (Trial 3 only)
  - `scenario_3_network_partition` (Trials 1, 2, 3)
  - `scenario_4_loss_1pct` (Trials 1, 2, 3)
  - `scenario_4_loss_5pct` (Trials 1, 2, 3)
  - `scenario_4_loss_10pct` (Trials 1, 2, 3)
  - `scenario_5_partition_recovery` (Trials 1, 2, 3)
  - `scenario_6_node_recovery` (Trial 1 only)

---

## 7. Confirmation of Compliance

- **No experiments were rerun during this audit.**
- **No raw CSV files were modified, overwritten, or deleted.**
- **All 6 required debug reports have been written to `results/fault_tolerance/debug/`.**
