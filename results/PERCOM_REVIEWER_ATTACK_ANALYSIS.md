# EdgeSync — PerCom Reviewer Attack Simulation & Vulnerability Analysis

**Audit Date:** `2026-09-01`  
**Reviewer Profile:** Highly skeptical senior IEEE PerCom / ACM SenSys / IEEE INFOCOM reviewer  
**Tone:** Rigorous, unsparing academic review designed to stress-test experimental validity, identify unbacked claims, and surface publication-blocking vulnerabilities.

---

## 1. Executive Summary of Reviewer Attack

The EdgeSync paper presents a decentralized edge computing architecture for geospatial ETA routing. While the core microbenchmark suite ($N > 19,000$ observations) demonstrates solid local execution speed and predictable scaling, a hostile reviewer will aggressively challenge the **environmental realism (loopback vs WAN)**, the **breadth of fault-tolerance claims**, and the **scope of eventual consistency guarantees**.

| Attack Category | Vulnerability Identified | Severity | Status in Existing Experiments | Missing Evidence / Defense Strategy |
| :--- | :--- | :---: | :--- | :--- |
| **A. Network Realism** | "All experiments run on localhost IPv4 loopback. Emulated sleep delays do not reflect true Internet jitter, packet loss, or WAN routing." | **HIGH** | Explicitly measured in Network Sensitivity ($N=9,000$), but on single-host loopback. | Bound claims to inter-service software delegation. State that physical multi-region WAN is future deployment work. |
| **B. Fault-Tolerance Scope** | "The paper claims comprehensive partition tolerance, but network partition and packet loss raw datasets produced HTTP 500 crashes." | **CRITICAL** | Acknowledged in debug audit; 14 runs corrupted by `TypeError` bug. | **MUST REMOVE** partition/loss claims from current submission. Retain only Peer Process Crash ($N=600$, 100% avail). |
| **C. Baseline Fairness** | "On loopback, Centralized is faster than EdgeSync Local by 0.25 ms. EdgeSync only wins if you assume massive cloud WAN latency." | **MEDIUM** | Directly measured in Controlled Latency ($N=900$). | Frame 0.25 ms as negligible software routing overhead that buys decentralized edge locality. |
| **D. Scalability Realism** | "Evaluated on a single laptop up to 64 concurrent threads. This does not prove planetary cloud scale." | **MEDIUM** | Proven up to $C=64$ ($650\text{ RPS}$, $N=6,300$). | Frame as edge-gateway / edge-cluster saturation (concurrency 1–64 per local micro-hub). |
| **E. Eventual Consistency** | "Gossip convergence is only verified on in-memory unit dictionaries, not continuous multi-writer WAN partitions." | **HIGH** | Mathematical model complete, but empirical validation prototype-only. | Frame CRDT set-union as an algebraic system model, not an empirical multi-datacenter consensus proof. |
| **F. Resource Evaluation** | "Process CPU/RSS sampled on host, not isolated cgroups on embedded edge devices (Raspberry Pi)." | **LOW** | RSS $< 180\text{ MB}$ logged in scalability runs. | Report as lightweight process footprint; do not claim superior hardware energy efficiency. |

---

## 2. Deep Dive: Reviewer Attack Scenarios & Defenses

### Attack 1: Network Realism & Loopback Emulation (Severity: HIGH)
- **Reviewer Critique:**  
  *"The authors claim to evaluate multi-region edge computing, yet Table X and Figure Y reveal that all services ran on `127.0.0.1`. Injecting software sleep delays into loopback sockets completely ignores TCP slow-start, BGP routing fluctuations, bufferbloat, and asymmetric cellular latency. Why should the pervasive computing community trust synthetic loopback results?"*
- **Existing Empirical Defense:**
  1. The Network Sensitivity experiment explicitly calibrated loopback overhead across $N=9,000$ requests, proving linear scaling ($R^2 = 0.9998$).
  2. The primary scientific question was isolating EdgeSync's software routing architecture from uncontrolled external Internet noise.
- **Vulnerability Gap:** Real-world WAN cross-traffic was not tested.
- **Required Paper Fix:** Explicitly qualify the title of Section V as *"Controlled Software Microbenchmarking under Calibrated Inter-Service Delays"* and list physical WAN deployment in the Limitations section.

### Attack 2: Fault Tolerance & Partition Claims (Severity: CRITICAL)
- **Reviewer Critique:**  
  *"The authors claim in Section I that EdgeSync provides 'complete fault-tolerance and partition resilience.' However, inspecting the raw data reveals that Scenario 3 (network partition) and Scenario 4 (packet loss) experienced total request failure (HTTP 500). How can the authors claim partition tolerance when the implementation crashed upon partition injection?"*
- **Existing Empirical Defense:**
  - Scenario 1 (Peer Crash) and Scenario 2 (Peer Unavailability) sustained 100.0% availability across 1,000 valid requests via automatic local fallback.
- **Vulnerability Gap:** Unhandled `TypeError` in `get_region([lat, lon])` caused ingress crashes in unpatched partition runs.
- **Required Paper Fix:** **ELIMINATE ALL CLAIMS of empirical network partition tolerance and packet loss resilience from the submission.** Defend ONLY Peer Process Crash resilience and Node Recovery.

### Attack 3: Centralized Baseline Advantage (Severity: MEDIUM)
- **Reviewer Critique:**  
  *"In Table I, Centralized achieves 1.35 ms P50 latency, whereas EdgeSync Local achieves 1.61 ms, and EdgeSync Cross-Region achieves 2.93 ms. EdgeSync is slower than the baseline in every zero-network condition! Why should anyone deploy a distributed architecture that adds latency?"*
- **Existing Empirical Defense:**
  - Centralized operates as a single monolithic process without geofencing checks. The 0.25 ms difference represents the microservice routing overhead.
  - In a pervasive setting, a centralized cloud server is located hundreds of kilometers away (adding $30-80\text{ ms}$ round-trip WAN transit), whereas EdgeSync executes on the local edge gateway.
- **Required Paper Fix:** Provide a clear latency decomposition chart showing that a $0.25\text{ ms}$ software routing cost is amortized by saving $>30\text{ ms}$ in wide-area network transit.

### Attack 4: Scalability & Production Realism (Severity: MEDIUM)
- **Reviewer Critique:**  
  *"A concurrency sweep of 1 to 64 workers on a single multi-core machine is a basic stress test, not a proof of distributed edge scalability. What happens when hundreds of edge nodes participate in gossip?"*
- **Existing Empirical Defense:**
  - Scalability benchmarks ($N=6,300$) prove that local edge processing sustains $650\text{ RPS}$ without thread deadlock or memory exhaustion.
- **Vulnerability Gap:** Large-scale gossip overhead ($M > 100$ nodes) was not simulated.
- **Required Paper Fix:** Explicitly scope scalability to *edge gateway request concurrency* ($C=1..64$) and frame multi-hundred-node gossip scaling as future hierarchical clustering work.

### Attack 5: Statistical Validity & Pseudoreplication (Severity: LOW)
- **Reviewer Critique:**  
  *"The authors pool 300 observations across 3 trials and report p-values with df=299. Because the same 100 requests were replayed, isn't this pseudoreplication?"*
- **Existing Empirical Defense:**
  - In addition to parametric paired $t$-tests, non-parametric Wilcoxon signed-rank tests and Holm-Bonferroni corrections were computed.
  - Trial-by-trial variance was strictly bounded (StdDev $< 0.3\text{ ms}$ across trials).
- **Required Paper Fix:** Report trial-aggregated means alongside pooled metrics, and emphasize effect sizes and percentiles (P50/P95) rather than relying solely on $p$-values.

---

## 3. Reviewer Attack Verdict & Pre-Submission Immunity Checklist

| Attack Target | Risk Level | Action Required to Immunize Paper |
| :--- | :---: | :--- |
| **Locality Claims** | **LOW** | Fully substantiated by $N=3,000$ dataset ($\rho = -1.0$). Safe for publication. |
| **Network Sensitivity** | **LOW** | Fully substantiated by $N=9,000$ dataset ($R^2 = 0.9998$). State loopback context clearly. |
| **Scalability Claims** | **LOW** | Fully substantiated by $N=6,300$ dataset (650 RPS). Safe for publication. |
| **Peer Crash Fallback** | **LOW** | Fully substantiated by $N=600$ dataset (100% availability). Safe for publication. |
| **Partition Tolerance** | **CRITICAL** | **REMOVE all empirical partition claims.** Do not include corrupted tables. |
| **Global Consistency** | **HIGH** | Present CRDT set-union as algebraic formal model; remove empirical multi-node claims. |
| **Resource Efficiency** | **MEDIUM** | Report footprint (< 180 MB RSS); do not claim edge-cloud energy superiority. |
