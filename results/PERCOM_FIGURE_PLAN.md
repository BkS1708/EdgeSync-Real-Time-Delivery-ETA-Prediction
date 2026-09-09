# EdgeSync — Final IEEE PerCom Figure Plan

**Audit Date:** `2026-09-01`  
**Status:** Canonical Figure Selection for IEEE PerCom 2027 Submission  
**Scope:** Specification of the 5 primary publication figures, data sources, captions, and exact locations in the manuscript.

---

## 1. Primary Publication Figure Matrix

| Figure Number | Filename & Path | Research Question | Canonical Raw Data Source | Primary Metric Displayed | Recommended Location |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **Figure 1** | [`locality_p50.png`](file:///results/locality/figures/locality_p50.png) | **RQ1 (Locality Sensitivity)** | [`results/locality/raw/`](file:///results/locality/raw/) ($N=3,000$) | P50 Median Latency (ms) across L90, L70, L50, L30, L10 vs Centralized Baseline | Section V-A (Locality Evaluation) |
| **Figure 2** | [`network_vs_p50.png`](file:///results/network_sensitivity/figures/network_vs_p50.png) | **RQ2 (Network Sensitivity & Shielding)** | [`results/network_sensitivity/raw/`](file:///results/network_sensitivity/raw/) ($N=9,000$) | Median Latency vs Configured Delay (0–50 ms) grouped by L90, L50, L10 | Section V-B (Network Sensitivity) |
| **Figure 3** | [`throughput_vs_concurrency.png`](file:///results/scalability/figures/throughput_vs_concurrency.png) | **RQ3 (Throughput Scalability)** | [`results/scalability/raw/`](file:///results/scalability/raw/) ($N=6,300$) | Throughput (Requests/Sec) across Concurrency $C \in \{1, 2, 4, 8, 16, 32, 64\}$ | Section V-C (Scalability Evaluation) |
| **Figure 4** | [`latency_vs_concurrency_p95.png`](file:///results/scalability/figures/latency_vs_concurrency_p95.png) | **RQ3 (Tail Latency Bounding)** | [`results/scalability/raw/`](file:///results/scalability/raw/) ($N=6,300$) | P95 Tail Latency (ms) across Concurrency $C=1$ to $C=64$ | Section V-C (Scalability Evaluation) |
| **Figure 5** | [`network_calibration.png`](file:///results/network_sensitivity/figures/network_calibration.png) | Methodological Rigor | [`results/network_sensitivity/statistics/`](file:///results/network_sensitivity/statistics/) ($N=9,000$) | Linear Regression calibration fit ($R^2 = 0.9998$) isolating loopback REST baseline | Section IV (Experimental Methodology) |

---

## 2. Detailed Figure Specifications & Captions

### Figure 1: Locality Sensitivity on Median Latency
- **Image File:** `results/locality/figures/locality_p50.png`
- **Why it belongs in the paper:** Visualizes the foundational premise of edge routing: high local clustering ($L90$) achieves near-baseline latency ($4.74\text{ ms}$ vs $4.19\text{ ms}$), while declining locality smoothly increases median latency with perfect rank correlation ($\rho = -1.0, p < 0.001$).
- **Recommended Caption:**  
  *Fig. 1. Median request latency (P50) across five spatial locality configurations ($L90$ to $L10$, $N=3,000$). EdgeSync demonstrates strong locality sensitivity ($\rho = -1.0$), matching centralized performance under high spatial clustering ($L90$) while incurring predictable inter-service forwarding delays as remote traffic increases.*

### Figure 2: Network Sensitivity & Locality Shielding
- **Image File:** `results/network_sensitivity/figures/network_vs_p50.png`
- **Why it belongs in the paper:** Highlights EdgeSync's network insulation effect: high spatial locality ($L90$) shields median user latencies ($1.55\text{ ms} \to 1.71\text{ ms}$) from severe inter-region delays, while remote-heavy traffic ($L10$) scales with linear precision ($R^2 = 0.9998$).
- **Recommended Caption:**  
  *Fig. 2. Impact of configured inter-service network delay (0–50 ms) on median latency across varying locality distributions ($N=9,000$). High spatial locality ($L90$) insulates the median user experience from remote network degradation, while low locality ($L10$) exhibits linear scaling ($R^2 = 0.9998$).*

### Figure 3: Concurrency Throughput Scaling
- **Image File:** `results/scalability/figures/throughput_vs_concurrency.png`
- **Why it belongs in the paper:** Proves that decentralized EdgeSync Local scales effectively under multi-threaded concurrency, reaching a peak throughput of $650.06\text{ RPS}$ at $C=8$ and sustaining $>520\text{ RPS}$ through $C=64$.
- **Recommended Caption:**  
  *Fig. 3. System throughput (requests per second) under increasing concurrency levels ($C=1$ to $C=64$, $N=6,300$). EdgeSync Local achieves peak throughput at $C=8$ ($650\text{ RPS}$) and matches centralized throughput scaling across all concurrency levels.*

### Figure 4: Tail Latency (P95) Scaling Under Load
- **Image File:** `results/scalability/figures/latency_vs_concurrency_p95.png`
- **Why it belongs in the paper:** Demonstrates that tail latency does not explode under concurrent load, remaining tightly bounded below $35\text{ ms}$ up to concurrency 16 for both Centralized and EdgeSync Local.
- **Recommended Caption:**  
  *Fig. 4. 95th percentile (P95) tail latency across concurrency levels ($C=1$ to $C=64$, $N=6,300$). EdgeSync Local maintains tightly bounded tail latencies comparable to the centralized baseline up to $C=16$, with graceful degradation at saturation loads.*

### Figure 5: Network Delay Emulator Calibration
- **Image File:** `results/network_sensitivity/figures/network_calibration.png`
- **Why it belongs in the paper:** Preempts reviewer skepticism regarding software delay injection by demonstrating near-perfect linear calibration ($R^2 = 0.9998$) and isolating $\approx 1.60\text{ ms}$ loopback socket transit.
- **Recommended Caption:**  
  *Fig. 5. Linear calibration of the inter-service network delay emulator ($R^2 = 0.9998, N=9,000$), demonstrating precise delay injection over IPv4 loopback with an empirical baseline REST overhead of $\approx 1.60-2.42\text{ ms}$.*

---

## 3. Supplementary Figures (For Appendix or Technical Report)

- **Fig S1:** `results/scalability/figures/memory_vs_concurrency.png` (Process RSS memory footprint $< 180\text{ MB}$).
- **Fig S2:** `results/scalability/figures/cpu_vs_concurrency.png` (Process CPU utilization $< 25\%$).
- **Fig S3:** `results/locality/figures/local_vs_remote.png` (Locality decomposition breakdown).
