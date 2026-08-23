# EdgeSync Research Dossier: Experiment Execution Checklist

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `15_EXPERIMENT_EXECUTION_CHECKLIST.md`

---

## 1. Priority Tiers Overview

To transform EdgeSync into an empirically validated paper, the following experiments must be executed.

---

## 2. Execution Checklist

### Priority 1: Critical Before Submission (Mandatory)

- [ ] **Exp 1: End-to-End Decision Latency Benchmarking (Intra vs Cross-Region vs Centralized)**
  - *Purpose:* Prove edge co-location reduces P95 decision latency compared to centralized cloud.
  - *Setup:* 3 regional nodes + 1 centralized server baseline. Send 10,000 requests using `locust`.
  - *Metrics:* Mean, Median, P95, P99 latency (ms).
  - *Expected Output Files:* `results/latency_raw.json`, `results/latency_summary.csv`.
  - *Graphs Required:* Cumulative Distribution Function (CDF) plot of latency.
  - *Tables Required:* Table comparing P50, P95, P99 across Intra, Cross, and Centralized setups.

- [ ] **Exp 2: System Scalability & Throughput Limits (RPS vs Concurrency)**
  - *Purpose:* Measure maximum requests per second (RPS) before response degradation.
  - *Setup:* Load test /custom_eta at 10, 50, 100, 500, 1000 concurrent clients.
  - *Metrics:* Throughput (RPS), Error rate (%), CPU (%), RAM (MB).
  - *Expected Output Files:* `results/scalability_results.csv`.
  - *Graphs Required:* Line plot: Concurrency (X-axis) vs Throughput RPS (Y-axis).

- [ ] **Exp 3: Gossip Convergence & State Divergence (Fixed vs Fixed + Traffic Noise)**
  - *Purpose:* Quantify time required for regional node state averages to converge across the ring.
  - *Setup:* Inject high ETA burst on EAST node; record `avg_eta` on all 3 nodes every 1 second.
  - *Metrics:* Time to convergence $T_{\text{conv}}$ (s), state variance $\sigma^2_{\text{state}}$.
  - *Graphs Required:* Line plot: Time (s) vs Node `avg_eta` for EAST, WEST, CENTRAL.

- [ ] **Exp 4: Network Payload & Control Overhead Profiling**
  - *Purpose:* Measure control message overhead of background gossip vs user payload traffic.
  - *Setup:* Capture TCP packets on ports 8000, 9000, 10000 during 1-hour load test.
  - *Metrics:* Control bytes, Data bytes, Overhead ratio (%).
  - *Tables Required:* Network traffic breakdown table.

---

### Priority 2: Strongly Recommended

- [ ] **Exp 5: Node Crash Failure & Recovery Time Measurement**
  - *Purpose:* Demonstrate fault tolerance during sudden microservice node failure.
  - *Setup:* Send 50 RPS; kill WEST node at $t=30\text{s}$; restart WEST node at $t=60\text{s}$.
  - *Metrics:* Error rate spike duration, recovery time $T_{\text{rec}}$ (s).
  - *Graphs Required:* Timeline plot: Time (s) vs HTTP Status 200 vs 500 count.

- [ ] **Exp 6: Traffic Model Sensitivity & ETA Validation**
  - *Purpose:* Verify ETA model responsiveness to distance ($1\text{ to }30\text{ km}$) and traffic levels.
  - *Metrics:* ETA (minutes) across distance steps under Low, Medium, High traffic.
  - *Graphs Required:* Grouped bar chart: Distance vs ETA by traffic level.

- [ ] **Exp 7: Ablation Study Execution (Partitioning & Gossip Disabled)**
  - *Purpose:* Quantify performance drops when key architectural components are ablated.
  - *Metrics:* Latency delta $\Delta L$, state divergence delta.
  - *Tables Required:* Master ablation comparison table.

---

### Priority 3: Optional / Future Work

- [ ] **Exp 8: Edge Node Hardware Benchmarking on Raspberry Pi / Jetson Nano**
  - *Purpose:* Measure CPU and memory footprint on physical resource-constrained ARM hardware.
  - *Metrics:* RAM footprint (MB), CPU core saturation (%).

- [ ] **Exp 9: Dynamic Gossip Frequency Adaptation ($\Delta t = 1\text{s to }30\text{s}$)**
  - *Purpose:* Find optimal gossip interval trade-off.
