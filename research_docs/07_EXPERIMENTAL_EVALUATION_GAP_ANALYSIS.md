# EdgeSync Research Dossier: Experimental Evaluation Gap Analysis

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `07_EXPERIMENTAL_EVALUATION_GAP_ANALYSIS.md`

---

## 1. Overview of Evaluation Gap

The current codebase contains **zero automated evaluation scripts, load testing frameworks, benchmark datasets, or log measurement parsers**. While the system functionality is implemented, it remains **IMPLEMENTED BUT NOT QUANTITATIVELY EVALUATED**.

To be accepted at IEEE PerCom 2027, the paper must transition from qualitative claims to rigorous, empirical, measurement-backed evaluation across 9 key experimental setups outlined below.

---

## 2. Blueprint for the 9 Core PerCom Experiments

### Experiment A: End-to-End Decision Latency Profiling
- **Objective:** Compare decision latency across three system setups:
  1. *Intra-Region EdgeSync* (Source and Destination in same region, e.g. EAST $\rightarrow$ EAST).
  2. *Cross-Region EdgeSync* (Source and Destination in different regions, e.g. EAST $\rightarrow$ WEST).
  3. *Centralized Cloud Baseline* (Single global server handling all spatial requests).
- **Metrics:** Mean, Median (P50), P95, P99, Minimum, and Maximum latency (in milliseconds).
- **Execution Methodology:** Use `locust` or `pytest-benchmark` to issue 10,000 HTTP POST requests under controlled concurrency (10, 50, 100 client connections). Instrument server response times using high-resolution timers (`time.perf_counter()`).

---

### Experiment B: Network Traffic & Payload Overhead
- **Objective:** Quantify network bandwidth consumption introduced by regional microservice delegation and background gossip state synchronization.
- **Metrics:** Total bytes sent/received, HTTP request rate, payload size per request, ratio of gossip control traffic to user data traffic.
- **Execution Methodology:** Capture network interface traffic on ports 8000, 9000, 10000 using `tcpdump` or `psutil.net_io_counters()` over a 1-hour continuous simulation.

---

### Experiment C: Gossip State Convergence & Divergence
- **Objective:** Evaluate how fast regional node ETA averages converge across the gossip ring after sudden step-changes in traffic or request volume.
- **Metrics:** Time to convergence $T_{\text{conv}}$ (seconds), message count to convergence, Root Mean Square Error (RMSE) between node states over time.
- **Expected Plot:** X-axis: Time (seconds); Y-axis: State Divergence $|A_E - A_W| + |A_W - A_C|$.
- **Execution Methodology:** Inject 100 high-ETA requests into EAST node only; record `avg_eta` across EAST, WEST, and CENTRAL nodes at 1-second intervals until $\Delta A < 0.01$.

---

### Experiment D: Fault Tolerance & Failure Recovery
- **Objective:** Measure system resilience during node crashes, network partitions, and node restarts.
- **Simulated Failures:**
  1. Graceful shutdown of WEST node (`port 9000`).
  2. Abrupt kill (`SIGKILL`) of CENTRAL node (`port 10000`).
  3. Temporary network isolation (blocking port 8000 $\rightarrow$ 9000 traffic).
- **Metrics:** Request success rate (%), service availability (%), recovery time $T_{\text{rec}}$ (seconds), ETA continuity error.

---

### Experiment E: System Scalability & Throughput Limits
- **Objective:** Benchmark throughput capacity under increasing concurrent load.
- **Independent Variables:** Concurrency level $C \in \{1, 10, 50, 100, 500, 1000\}$ requests/sec.
- **Metrics:** Throughput (Requests Per Second - RPS), median response latency (ms), CPU utilization (%), RAM usage (MB).
- **Execution Methodology:** Execute load test generator against `/custom_eta` endpoint using `wrk` or `locust`.

---

### Experiment F: Traffic Model Sensitivity
- **Objective:** Validate ETA sensitivity under varying distance ranges and traffic levels.
- **Setup:** Measure computed ETA across distances $d \in \{1, 5, 10, 15, 20, 25, 30\}\text{ km}$ under Low (35 km/h), Medium (25 km/h), and High (15 km/h) traffic.
- **Expected Plot:** X-axis: Distance (km); Y-axis: ETA (minutes) with grouped bars for Low, Medium, High traffic.

---

### Experiment G: Cross-Region Delegation Overhead
- **Objective:** Isolate the exact microservice network latency penalty caused by cross-region REST calls.
- **Metrics:** Intra-region latency $L_{\text{intra}}$ vs Cross-region latency $L_{\text{cross}}$.
- **Overhead Formula:** $\Delta L_{\text{cross}} = L_{\text{cross}} - L_{\text{intra}}$.

---

### Experiment H: Edge Node Resource Utilization
- **Objective:** Monitor hardware resource overhead per regional microservice.
- **Metrics:** Percentage CPU usage, memory footprint (RSS in MB), thread count, open socket count.
- **Execution Methodology:** Use `psutil` background process to sample FastAPI process stats every 1 second during stress testing.

---

### Experiment I: Reproducibility & Random Noise Audit
- **Objective:** Assess the impact of stochastic noise in rider proximity (`utils.py:L50`) and food prep time (`utils.py:L62`).
- **Execution Methodology:** Add deterministic random seeding (`random.seed(42)`) to verify reproducible ETA outputs across experimental runs.
