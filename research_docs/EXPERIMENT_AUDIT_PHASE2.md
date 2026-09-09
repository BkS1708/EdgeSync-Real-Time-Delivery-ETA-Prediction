# EdgeSync Phase 2: Experimental Audit & Methodological Reform

**Target Venue:** IEEE PerCom 2027  
**Document Purpose:** Rigorous audit of Phase 1 experimental methodologies, identification of flaws, classification of severity, and definition of required scientific fixes.

---

## 1. Executive Summary of Audit Findings

The Phase 1 implementation successfully established the microservice framework, mathematical state algebra, telemetry logging, and baseline servers. However, a critical methodological audit reveals several experimental flaws that invalidate previous quantitative metrics (such as the claimed 41% latency reduction and 2020 ms ablation numbers):

1. **Artificial Latency Masking:** Cross-region REST calls in `east.py`, `west.py`, `central.py` enforced a hard `GOSSIP_TIMEOUT = 2.0s` (`requests.post(..., timeout=2.0)`). Cross-region requests timed out and fell back to local calculations at ~2020 ms, masking real network routing and computation latencies.
2. **Workload Mismatch:** Baseline comparisons independently generated random request workloads rather than replaying an identical, hash-verified workload set.
3. **Small Sample Sizes & Unmatched Samples:** Latency experiments used unbalanced sample counts ($N_{\text{intra}}=31$, $N_{\text{cross}}=69$) without cold-start/warm-up separation.
4. **Instantaneous CPU Sampling Flaw:** Process CPU usage was sampled instantaneously (`process.cpu_percent(interval=None)`), returning `0.0%` instead of averaging CPU load over the benchmark duration.
5. **Inadequate Scalability Workload:** Scalability testing peaked at 20 concurrent threads under light synthetic load without identifying the true saturation or latency collapse point.
6. **Localhost Emulation Disclosures:** All 3 edge nodes ran on a single physical host on `localhost`, which does not reflect WAN/cellular network latency without explicit network delay emulation.

---

## 2. Comprehensive Experiment Audit Table

| Experiment | Current Method (Phase 1) | Flaw / Vulnerability Identified | Severity | Required Methodological Fix (Phase 2) |
| :--- | :--- | :--- | :--- | :--- |
| **Latency** | 100 requests generated on-the-fly; uncalibrated REST timeouts; unmatched samples ($N=31$ vs $N=69$). | Cross-region calls hit 2.0s timeout fallback; non-identical requests compared across baselines; no cold-start removal. | **CRITICAL** | Replay single hashable $N \ge 1000$ workload (`benchmark_workload.json`); separate system overhead ($L_{\text{sys}}$) from business logic ($L_{\text{domain}}$); remove warm-up samples; compute P50/P90/P95/P99 with 95% CIs and paired $t$-tests. |
| **Throughput** | 60 requests over 20 workers using Python `ThreadPoolExecutor`. | Workload size too small ($N=60$); fails to reach server saturation or latency collapse point. | **HIGH** | Perform load sweep ($1, 2, 5, 10, 20, 50, 100, 200 \text{ req/sec}$) with $N \ge 1000$ requests per load point; measure offered load vs achieved throughput & error rate. |
| **Scalability & Concurrency** | Concurrency levels $[1, 5, 10, 20]$ tested on single process. | Limited concurrency sweep; CPU/RAM sampled snapshot-style; does not test process thread pool exhaustion. | **HIGH** | Sweep concurrency ($1, 2, 4, 8, 16, 32, 64, 128$ workers); sample CPU over full interval (`psutil`); plot latency CDF and resource footprint vs concurrency. |
| **Gossip Convergence** | Injected 10 observations into EAST; tracked 10 ticks of 1s sleeps. | Fixed single ring topology; no background load during convergence; unmeasured payload byte overhead. | **MEDIUM** | Evaluate convergence under Ring, Fully Connected, and Peer List topologies across $N=3, 5, 10, 20$ simulated nodes; measure time, message count, bytes, and state divergence. |
| **Fault Tolerance** | Sent requests to EAST during local loop; recorded status codes. | Termed local timeout fallback "fault resilience"; no true node crash, network partition, or recovery phase tested. | **CRITICAL** | Test controlled failure matrix: Peer crash, packet drops, network partition, partition recovery. Measure availability, state divergence, lost messages, and recovery timeline. |
| **Ablation Studies** | Re-ran requests against EAST node with 2.0s timeout. | All 5 ablation variants returned identical ~2020 ms latency because request timeout masked underlying feature toggles. | **CRITICAL** | Implement true feature toggles (Partitioning ON/OFF, Gossip ON/OFF, Delegation ON/OFF, Traffic Model ON/OFF, Noise ON/OFF); measure pure system latency ($L_{\text{sys}}$). |
| **Resource Usage** | Sampled instantaneous CPU (`interval=None`). | CPU reported as `0.0%` or static snapshot; RAM did not account for background thread allocation. | **HIGH** | Implement interval-based CPU profiling over full experiment duration per process node (`psutil.Process.cpu_percent(interval=duration)`). |
| **Network Emulation** | Local TCP sockets over `localhost` loopback. | 0 ms network delay distorts cross-region delegation costs compared to real geographically distributed edge nodes. | **HIGH** | Build network emulation proxy harness supporting profiles: `Local edge` (1ms), `Metro edge` (5ms), `Regional` (20ms), `Degraded` (50ms), `High latency` (100ms), `Severe` (200ms), and packet loss (0–5%). |
| **Partitioning & Locality** | Fixed geofence (`lat < 19.05`, `lon < 72.85`). | Locality ratio not systematically varied; dynamic partitioner unbenchmarked. | **HIGH** | Sweep request spatial locality (90%, 70%, 50%, 30%, 10% local); compare Static Geofencing vs Dynamic Grid Partitioning under uniform & hotspot traffic. |
| **Topology Trade-offs** | Tested default ring topology only. | No comparative evaluation of network overhead vs convergence speed across topologies. | **MEDIUM** | Benchmark Ring vs Fully Connected vs Peer List; plot Gossip Interval vs Convergence Time and Communication Overhead (bytes/sec). |
| **Sync Interval** | Hardcoded default interval (5.0s). | No empirical trade-off curve between sync frequency, network bandwidth, and state staleness. | **MEDIUM** | Sweep sync interval ($0.5\text{s}, 1\text{s}, 2\text{s}, 5\text{s}, 10\text{s}, 20\text{s}$); plot interval vs convergence time, network traffic, and CPU utilization. |

---

## 3. Methodological Reform Plan

To guarantee IEEE PerCom publication standards, all Phase 2 experiments will enforce:
1. **Single Hashable Workload Dataset:** All baselines and variants will process the exact same `experiments/workloads/benchmark_workload.json` dataset (hashed via SHA-256).
2. **Decomposed Microsecond Latency Logging:** Every HTTP response will explicitly return:
   - `L_total` (End-to-End Latency)
   - `L_sys` (Pure System / REST Framework / Routing Latency)
   - `L_domain` (Domain ETA Calculation Math)
   - `L_net` (Cross-Region Network Transit Time)
3. **Warm-Up / Cold-Start Isolation:** First 50 requests will be discarded as warm-up; cold-start latency will be measured and reported separately.
4. **Reproducibility Metadata:** Every run will emit `experiment_metadata.json` containing Git commit, random seed, hardware specs, OS, Python version, and workload SHA-256 hash.
