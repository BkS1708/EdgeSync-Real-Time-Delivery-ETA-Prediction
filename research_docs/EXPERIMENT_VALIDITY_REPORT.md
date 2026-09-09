# EdgeSync: Comprehensive Experiment Validity Report

**Target Venue:** IEEE PerCom 2027  
**Document Purpose:** Detailed validity audit for each flagship experiment suite, documenting hypotheses, variables, sample sizes, statistical methodologies, empirical outcomes, and safe scientific interpretations.

---

## 1. Flagship Experiment 1: Matched Decision Latency Benchmark

- **Hypothesis:** Decentralized edge decision-making reduces pure system latency ($L_{\text{sys}}$) compared to a centralized cloud architecture by eliminating cross-region network transit and routing bottlenecks.
- **Independent Variable:** System Architecture (`Intra-Region EdgeSync`, `Cross-Region EdgeSync`, `Full Cluster`, `EdgeSync w/o Gossip`, `EdgeSync w/o Partitioning`, `Centralized Baseline`).
- **Dependent Variables:** End-to-End Latency ($L_{\text{total}}$ ms), Pure System Latency ($L_{\text{sys}}$ ms), Cross-Node Network Latency ($L_{\text{net}}$ ms).
- **Baseline:** Centralized Baseline (`http://localhost:8000/custom_eta` with `partitioning_enabled=False`, `delegation_enabled=False`).
- **Workload Dataset:** `experiments/workloads/benchmark_workload.json` ($N=1000$ deterministic requests, SHA-256 hash verified).
- **Sample Size & Warm-up:** $N=1000$ requests per architecture. First 50 requests discarded as warm-up; cold-start analyzed separately.
- **Statistical Method:** Paired Welch's $t$-test ($p < 0.05$), 95% Confidence Intervals, P50/P90/P95/P99 percentiles.
- **Empirical Results:**
  - **Intra-Region EdgeSync:** $L_{\text{sys}} = 2.1\text{ ms}$, P95 = $3.8\text{ ms}$
  - **Centralized Baseline:** $L_{\text{sys}} = 5.4\text{ ms}$, P95 = $8.2\text{ ms}$
  - **p-value vs Centralized:** $p = 0.000012 < 0.001$ (Statistically Significant)
- **Limitations:** Experiments executed on single multi-core host using loopback network sockets. Real-world WAN/cellular latency is emulated via microsecond delays.
- **Safe Scientific Interpretation:** EdgeSync significantly reduces microservice orchestration overhead ($L_{\text{sys}}$). When evaluating total wall-clock time, domain preparation simulation ($L_{\text{domain}}$) dominates.

---

## 2. Flagship Experiment 2: System Scalability & Offered Load Sweep

- **Hypothesis:** EdgeSync maintains bounded P95 latency and zero request drop rates under load up to the node hardware saturation limit.
- **Independent Variables:** Offered Load ($1, 5, 10, 20, 50, 100, 200\text{ req/sec}$), Concurrency Workers ($1, 2, 4, 8, 16, 32, 64, 128$).
- **Dependent Variables:** Achieved Throughput (RPS), P95 Latency (ms), HTTP Error Rate (%), CPU Utilization (%), RAM Allocation (MB).
- **Baseline:** Single-thread baseline vs Multi-worker thread pool execution.
- **Workload Dataset:** Paced replay of `benchmark_workload.json` ($N=1000$ requests per load point).
- **Sample Size:** 8 concurrency points $\times$ 7 load points = 56 measurement runs.
- **Statistical Method:** Offered vs Achieved throughput regression and P95 latency collapse threshold determination.
- **Empirical Results:**
  - **Maximum Sustainable Throughput:** **~95 req/sec**
  - **Saturation Threshold:** 100 req/sec (P95 latency rises above 50 ms)
  - **Error Rate at 200 req/sec:** < 1.5%
- **Limitations:** Process thread pool limits on Windows Uvicorn server constrain single-process concurrency.
- **Safe Scientific Interpretation:** EdgeSync scales predictably up to ~95 req/sec per node cluster. Scaling beyond 100 req/sec requires multi-process worker scaling.

---

## 3. Flagship Experiment 3: Controlled Fault Matrix & Resilience

- **Hypothesis:** EdgeSync provides uninterrupted service availability during node crashes or network partitions via local parameter fallback.
- **Independent Variable:** Failure Type (Node Crash, Peer Drop, REST Delay, Packet Loss, Network Partition, Node Restart).
- **Dependent Variables:** HTTP Availability Rate (%), State Recovery Duration (seconds), State Divergence Index.
- **Scenarios Tested:** 9 distinct fault conditions ($N=100$ requests per scenario).
- **Empirical Results:**
  - **Request Availability:** **100.0%** across all scenarios (zero HTTP 500 crashes).
  - **State Recovery Time:** **2.6s** post-partition recovery via set-union gossip sync.
- **Limitations:** Fallback calculations use local historical state, which may have reduced accuracy during prolonged peer isolation.
- **Safe Scientific Interpretation:** EdgeSync achieves high availability through **Graceful Degradation**, ensuring system responsiveness even when peer nodes are unreachable.

---

## 4. Flagship Experiment 4: Component Ablation Study

- **Hypothesis:** Disabling key architecture modules (Partitioning, Delegation, Gossip, Traffic Model) will measurably degrade pure system efficiency or state freshness.
- **Independent Variable:** Enabled Feature Toggles (`PARTITIONING`, `DELEGATION`, `GOSSIP`, `TRAFFIC_MODEL`, `PREP_NOISE`).
- **Dependent Variable:** Pure System Overhead ($L_{\text{sys}}$ ms), State Freshness.
- **Sample Size:** $N=200$ matched requests per variant across 6 architectural configurations.
- **Empirical Results:**
  - **Full EdgeSync:** $L_{\text{sys}} = 2.1\text{ ms}$
  - **Ablation 1 (Partitioning OFF):** $L_{\text{sys}} = 4.8\text{ ms}$ (+128% overhead increase)
  - **Ablation 2 (Cross-Delegation OFF):** $L_{\text{sys}} = 1.9\text{ ms}$ (Faster local math, but stale state)
- **Safe Scientific Interpretation:** Geographic partitioning is the single most critical component for minimizing cross-node REST delegation latency.

---

## 5. Summary of Experimental Integrity Guarantees

1. **Deterministic Replayability:** All 6 runners replayed `experiments/workloads/benchmark_workload.json` with verified SHA-256 hash `cee0014768734e19c804972daaaf69d846faacf96f00fd62a3eef429466dc8ac`.
2. **Warm-Up Isolation:** 50 initial requests were discarded in every run to prevent JIT/connection pool cold-start distortion.
3. **Interval CPU Profiling:** Continuous `psutil` sampling eliminated the `0.0%` CPU artifact.
4. **Clean Results Directory:** All Phase 3 data is cleanly isolated under `results/phase3/`.
