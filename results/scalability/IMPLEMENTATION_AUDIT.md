# EdgeSync Scalability Experiment — Implementation & Infrastructure Audit

**Audit Date/Time:** `2026-08-25 18:05:00`  
**Objective:** Thorough inspection of codebase infrastructure, measurement instrumentation, and lifecycle management for the PerCom Concurrency & Scalability Experiment.

---

## 1. Existing Components Reused

1. **Regional Service Microservices:**
   - [`east.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py) (`http://127.0.0.1:8000`): Ingress coordinator, local compute, and remote delegation client.
   - [`west.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/west.py) (`http://127.0.0.1:9000`): Western regional compute peer for cross-region delegation (`/calc_delivery`).
   - [`central.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/central.py) (`http://127.0.0.1:10000`): Central regional compute peer.
2. **Centralized Baseline Model:**
   - Invoked via `http://127.0.0.1:8000/custom_eta` with `partitioning_enabled=False` and `delegation_enabled=False`.
3. **Core Utility Library:**
   - [`utils.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py): Haversine distance, speed model, dynamic traffic, prep time calculation, and observation management.
4. **Configuration Layer:**
   - [`config.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/config.py): Node URLs mapped explicitly to IPv4 loopback (`127.0.0.1`), Mumbai geographic bounding zones, and feature toggles.
5. **Statistical Utilities:**
   - [`experiments/analysis/statistics.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/experiments/analysis/statistics.py): `calculate_stats()` computing count, min, max, mean, median, stddev, P50, P90, P95, P99, and 95% confidence intervals.
6. **Process Lifecycle Management:**
   - Subprocess orchestration with Uvicorn worker management, `/health` endpoint polling, and reliable Windows port binding reclamation.

---

## 2. Existing Instrumentation Reused

1. **Microsecond Precision Timers:**
   - Monotonic clock `time.perf_counter()` measuring request dispatch to response reception.
2. **Decomposed Latency Metrics:**
   - Direct extraction of `latency_ms.total`, `latency_ms.system`, `latency_ms.network`, and `latency_ms.computation` from service JSON payloads.
3. **Deterministic Workload Generation:**
   - Hash-locked workload generation (`SHA-256` of canonical JSON request arrays) with uniform spatial coordinates across defined Mumbai zones.
4. **Thread-Safe Session Pooling:**
   - Thread-local `requests.Session()` pools for concurrency execution to isolate HTTP/1.1 socket connections per worker thread.

---

## 3. Existing Statistics & Plotting Utilities Reused

1. **Statistical Aggregation:**
   - Calculation of P50, P90, P95, P99, and standard deviation directly from raw measured distributions (excluding warm-up).
2. **Hypothesis Testing:**
   - Wilcoxon signed-rank test for paired request-level latency comparisons between Centralized and EdgeSync architectures.
   - Holm-Bonferroni family-wise error rate correction for multi-concurrency comparisons.
3. **Matplotlib Visualizations:**
   - IEEE-compliant publication figures (300 DPI, clean typography, explicit axis units, no misleading 3D projections).

---

## 4. New Components Required for Scalability

1. **Scalability Experiment Runner (`experiments/runners/run_scalability_experiment.py`):**
   - High-throughput thread pool orchestrator supporting concurrency levels $C \in \{1, 2, 4, 8, 16, 32, 64\}$.
   - Benchmark duration timers measuring exact throughput ($\text{req/sec} = \frac{N_{\text{success}}}{\Delta t_{\text{benchmark}}}$).
   - Checkpointing engine resuming interrupted runs without rerunning completed CSVs.
2. **Smoke Test Runner (`experiments/runners/run_scalability_smoke_test.py`):**
   - Lightweight pre-flight validation (concurrency 1, 4, 16; 20 requests; 1 trial) verifying socket stability before full matrix execution.
3. **Resource Monitor:**
   - `psutil` sampling for process CPU % and RSS RAM utilization across regional nodes during concurrent load.

---

## 5. Scalability-Relevant Bugs Discovered & Addressed

1. **Old Script Incompatibilities in `run_scalability_experiment.py`:**
   - Used `localhost` (causing IPv6 fallback delays on Windows) $\to$ **Updated to `127.0.0.1`**.
   - Concurrency sweep used arbitrary sample sizes $\to$ **Standardized to exact $100\text{ measured} + 20\text{ warmup}$ requests**.
   - Did not separate EdgeSync Local vs. EdgeSync Cross-Region $\to$ **Added explicit 3-way architectural comparison**.
2. **Statistics Integrity Safeguard:**
   - Ensured availability is calculated strictly as $\frac{\text{Success}}{\text{Total}} \times 100$ and never hard-coded.

---

## 6. Exact Files Requiring Modification / Creation

- **New:** [`experiments/runners/run_scalability_smoke_test.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/experiments/runners/run_scalability_smoke_test.py)
- **New/Updated:** [`experiments/runners/run_scalability_experiment.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/experiments/runners/run_scalability_experiment.py)
- **New:** `results/scalability/IMPLEMENTATION_AUDIT.md`
- **New:** `results/scalability/MEASUREMENT_FIXES.md`
- **New:** `results/scalability/smoke_test/SMOKE_TEST_REPORT.md`
- **New:** `results/scalability/SCALABILITY_DATA_AUDIT.md`
- **New:** `results/scalability/REPRODUCIBILITY.md`
- **New:** `results/scalability/SCALABILITY_EXPERIMENT_REPORT.md`
