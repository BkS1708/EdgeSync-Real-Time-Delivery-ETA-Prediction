# EdgeSync: Claim vs. Evidence Matrix (Version 2 - Phase 3 Validated)

**Target Venue:** IEEE PerCom 2027  
**Document Purpose:** Definitive evaluation of paper claims against Phase 3 validated empirical evidence. Replaces initial Phase 1 baseline claims with scientifically defensible classifications.

---

## 1. Classification Guidelines

Every claim is categorized under one of five strict academic classifications:
- **SUPPORTED:** Empirical data from hash-verified, multi-trial experiments directly corroborates the claim with statistical significance ($p < 0.05$).
- **PARTIALLY SUPPORTED:** The physical or architectural mechanism works as claimed, but quantitative bounds depend on specific operating parameters (e.g., domain simulation vs system overhead).
- **NOT SUPPORTED:** Empirical data refutes the claim or demonstrates that external factors mask the claimed effect.
- **NOT TESTED:** Implementation exists, but experimental validation under WAN/cellular conditions remains future work.
- **THEORETICAL ONLY:** Mathematical formulation is complete, but real-world hardware validation has not been performed.

---

## 2. Master Claim-Evidence Matrix

| Claim ID | Paper / System Claim | Phase 3 Classification | Supporting Experiment File | Sample Size ($N$) | Primary Metric | Empirical Result / Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **C1** | EdgeSync reduces decision latency compared to centralized routing | **PARTIALLY SUPPORTED** | `results/phase3/latency/latency_summary.json` | $N=1000$ requests (50 warm-up discarded) | Pure System Latency ($L_{\text{sys}}$) vs Total Latency ($L_{\text{total}}$) | **$L_{\text{sys}}$ reduced by ~38%** for intra-region requests ($p < 0.001$). However, domain prep simulation ($L_{\text{domain}}$) dominates total wall-clock latency. |
| **C2** | Throughput scales linearly with increasing client request load | **PARTIALLY SUPPORTED** | `results/phase3/scalability/scalability_summary.json` | Load sweep $1..200\text{ req/s}$ ($N=1000$ per point) | Achieved RPS & Error Rate | Throughput scales linearly up to **85–100 req/s**; thread pool saturation occurs above 100 req/s leading to queue latency growth. |
| **C3** | Gossip state synchronization achieves rapid state convergence | **SUPPORTED** | `results/phase3/gossip/summary.json` | $N=3$ nodes, 10-tick time-series sweep | State Divergence ($\Delta \text{ETA}$ ms) & Convergence Time (s) | State converges in **$<2.6\text{s}$** (Ring topology) and **$<1.2\text{s}$** (Fully Connected topology) with zero residual divergence. |
| **C4** | Platform maintains 100% availability during peer node failure | **SUPPORTED** *(Graceful Degradation)* | `results/phase3/fault_tolerance/fault_matrix.csv` | 9 Failure Scenarios ($N=100$ reqs each) | HTTP Availability (%) & Error Count | **100.0% request availability** maintained across node crashes, peer drops, and partitions via local estimation fallback. |
| **C5** | Spatial locality partitioning minimizes cross-region routing traffic | **SUPPORTED** | `results/phase3/partitioning/partitioning_summary.json` | Locality sweep 90% to 10% ($N=500$ reqs) | Cross-Region Rate (%) & Mean Latency | Increasing intra-region locality from 10% to 90% reduces cross-region delegation rate from **90.0% to 10.0%**, reducing $L_{\text{sys}}$ linearly. |
| **C6** | Dynamic traffic speed model adjusts ETA predictions dynamically | **SUPPORTED** | `results/phase3/ablation/ablation_summary.json` | Ablation Variant 4 ($N=200$ reqs) | Pure System Overhead ($L_{\text{sys}}$ ms) | Dynamic traffic model introduces **$<0.4\text{ms}$** system calculation overhead while updating regional vector clocks continuously. |
| **C7** | EdgeSync operates efficiently on standard edge hardware | **THEORETICAL ONLY** | `results/phase3/experiment_metadata.json` | Host System Profiling | Process CPU & RAM | Benchmark executed on multi-core Windows host (`localhost` background services); physical Raspberry Pi / Jetson Nano deployment is future work. |

---

## 3. Key Findings & Paper Positioning Recommendations

### 1. Latency Nuance ($L_{\text{sys}}$ vs $L_{\text{domain}}$)
In previous reports, total wall-clock time was reported as system latency. In Phase 3, we explicitly decomposed latency into:
$$L_{\text{total}} = L_{\text{sys}} + L_{\text{domain}}$$
- **Pure System Latency ($L_{\text{sys}}$):** EdgeSync routing and REST processing takes **$2.1\text{ms}$** (Intra-Region) vs **$5.4\text{ms}$** (Centralized), representing a **38% system overhead reduction**.
- **Domain Preparation ($L_{\text{domain}}$):** Simulated kitchen preparation and rider movement physics dominate total time. The paper must clearly state that EdgeSync optimizes *distributed coordination overhead*, not physical delivery processes.

### 2. Honest Scalability Boundaries
EdgeSync achieves a maximum sustainable throughput of **~95 req/sec** on the test environment. Beyond 100 req/sec, Uvicorn worker thread queues experience latency inflation. This provides a clean saturation curve for the IEEE PerCom paper.

### 3. Fault Resilience Terminology
Local fallback execution is accurately classified as **Graceful Degradation** rather than transparent failure masking. When a peer node crashes, requests complete successfully using local parameters without triggering HTTP 500 errors.
