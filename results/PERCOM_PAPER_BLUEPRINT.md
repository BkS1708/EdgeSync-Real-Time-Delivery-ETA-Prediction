# EdgeSync — Final IEEE PerCom Paper Structure Blueprint

**Audit Date:** `2026-09-01`  
**Status:** Comprehensive Manuscript Blueprint for IEEE PerCom 2027  
**Target Venue:** 25th IEEE International Conference on Pervasive Computing and Communications (PerCom)  
**Scope:** Section-by-section drafting guide detailing exact narrative arguments, supporting canonical experiments, figures, tables, precise metrics, and forbidden assertions.

---

## 1. Title & Abstract

### 1. Title
- **Recommended Title:** *EdgeSync: Locality-Aware Decentralized Edge Microservices for Low-Latency Spatial Estimation*
- **Alternative:** *EdgeSync: A Decentralized, Fault-Resilient Edge Computing Architecture for Geographic ETA Prediction*

### 2. Abstract
- **What to Write:** Motivation (centralized cloud routing bottlenecks, WAN latency variability in pervasive mobility); Proposed solution (EdgeSync decentralized edge microservice architecture with spatial partitioning, autonomous fallback, and idempotent state synchronization); Key empirical results.
- **Exact Numbers to Quote:**
  - Median local software routing latency: $1.609\text{ ms}$ (P50) with only $0.25\text{ ms}$ software overhead over monolithic baseline.
  - Locality sensitivity: Spearman $\rho = -1.0, p < 0.001$ ($4.74\text{ ms}$ at L90 vs $10.15\text{ ms}$ at L10 across $N=3,000$).
  - Network delay scaling & shielding: Linear remote scaling ($R^2 = 0.9998$) with median latency shielded ($1.55\text{ ms} \to 1.71\text{ ms}$) under high locality ($N=9,000$).
  - Concurrency scaling: Peak throughput of $650.06\text{ RPS}$ at $C=8$ and sustained $>520\text{ RPS}$ up to $C=64$ ($N=6,300$).
  - Fault resilience: $100.0\%$ request availability maintained during peer process crashes via autonomous local fallback ($N=600$).
- **Claims to Avoid:** ❌ No "41% cloud latency reduction", no "complete WAN partition tolerance", no "energy efficiency".

---

## 2. Introduction, Motivation & Problem Statement

### 3. Introduction
- **What to Write:** Pervasive mobile applications (ride-hailing, autonomous fleet navigation, micro-mobility) demand sub-second, highly reliable spatial predictions. Centralized cloud architectures suffer from high WAN transit delays ($30-80\text{ ms}$), bandwidth congestion, and single points of failure. Edge computing promises low latency by moving execution to network boundaries, but cross-region requests and peer node failures introduce routing complexity.
- **Core Contribution:** (1) Decentralized spatial geofencing architecture; (2) Autonomous local fallback mechanism; (3) Multi-trial evaluation across $>19,200$ controlled requests.

### 4. Motivation & 5. Problem Statement
- **What to Write:** Formalize the spatial routing problem. A request with origin/dest coordinates $(o, d)$ submitted at edge node $e_i$ requires fast local processing if $d \in \text{Region}(e_i)$, or predictable delegation if $d \in \text{Region}(e_j)$. Define failure scenarios where $e_j$ is unreachable.

---

## 3. System Architecture, Design & Formal Models

### 6. System Architecture & 7. EdgeSync Design
- **What to Write:** Multi-region microservice architecture (FastAPI ASGI workers), geofence partitioner, persistent HTTP/1.1 connection pools, asynchronous request dispatcher.

### 8. Spatial Locality Model
- **What to Write:** Mathematical definition of spatial locality $\alpha = \frac{|\text{Local Requests}|}{|\text{Total Requests}|}$. Formulate why $L90$ insulates the cluster from WAN degradations.

### 9. Gossip Synchronization & State Reconciliation
- **What to Write:** Formulate the distributed observation store as a state-based CRDT (Conflict-free Replicated Data Type) using vector clocks and set-union merging ($A \cup A = A$). Detail idempotence, commutativity, and associativity guarantees.
- **Supporting Document:** [`research_docs/DISTRIBUTED_STATE_MODEL.md`](file:///research_docs/DISTRIBUTED_STATE_MODEL.md).

### 10. Routing & Autonomous Fallback Mechanism
- **What to Write:** Sequence diagram of request flow: Ingress $\to$ Geofence check $\to$ Local ETA / Remote delegation $\to$ Catch connection timeout / HTTP 503 $\to$ Autonomous local fallback execution.

---

## 4. Experimental Methodology & Results

### 11. Experimental Methodology
- **Supporting Table:** **Table I** (Experimental Parameters).
- **Supporting Figure:** **Figure 5** (`network_calibration.png`).
- **What to Write:** Testbed setup over calibrated IPv4 loopback, high-resolution monotonic timing (`time.perf_counter()`), hash-verified deterministic workloads ($N=1,000$, seed=42), 20 isolated warmup requests. State that inter-service network delay is emulated over loopback sockets.

### 12. Experimental Results
- **Supporting Tables:** **Table II** (Baseline Latency), **Table III** (Locality & Network), **Table IV** (Scalability).
- **Supporting Figures:** **Figure 1** (`locality_p50.png`), **Figure 2** (`network_vs_p50.png`), **Figure 3** (`throughput_vs_concurrency.png`), **Figure 4** (`latency_vs_concurrency_p95.png`).
- **Key Subsections:**
  1. *Baseline Latency Decomposition:* Discuss 0.25 ms software routing overhead (Table II).
  2. *Locality Sensitivity (RQ1):* Discuss monotonic scaling ($\rho = -1.0$) and Table III / Fig 1.
  3. *Network Delay Sensitivity & Shielding (RQ2):* Discuss linear model ($R^2 = 0.9998$) and L90 shielding in Fig 2.
  4. *Concurrency & Scalability (RQ3):* Discuss 650 RPS throughput, bounded P95 tail latency, and statistical equivalence at $C=4$ ($p = 0.0544$) in Fig 3 & 4.

---

## 5. Fault Tolerance, Discussion, Limitations & Conclusion

### 13. Fault and Recovery Evaluation
- **Supporting Table:** **Table V** (Fault Tolerance & Fallback).
- **What to Write:** Scenario 1 (Peer Crash) and Scenario 2 (Peer Unavailability) results ($N=1,000$ valid requests, 100% availability, 250 fallback activations). Scenario 6 Node Recovery demonstrating seamless restoral of remote delegation.
- **Claims to Avoid:** ❌ Do NOT claim empirical network partition or packet loss tolerance.

### 14. Discussion
- **What to Write:** Architectural trade-offs between local edge execution and cross-region delegation. Practical deployment considerations on Road-Side Units (RSUs) and 5G Multi-access Edge Computing (MEC) gateways.

### 15. Limitations
- **Supporting Document:** [`results/PERCOM_LIMITATIONS.md`](file:///results/PERCOM_LIMITATIONS.md).
- **What to Write:** Explicitly disclose loopback socket environment, in-memory volatile observation storage, single-host process concurrency, and lack of physical multi-continent WAN deployment.

### 16. Related Work & 17. Conclusion
- **Related Work:** Edge-assisted microservices, geospatial ETA prediction (e.g., centralized OSRM, Valhalla), CRDTs and epidemic protocols.
- **Conclusion:** Summary of contributions and verified quantitative findings.
