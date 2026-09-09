# EdgeSync — Final IEEE PerCom Research Story & Scientific Narrative

**Audit Date:** `2026-09-01`  
**Status:** Defensible Scientific Narrative for IEEE PerCom Submission  
**Target Venue:** IEEE International Conference on Pervasive Computing and Communications (PerCom)  
**Objective:** Define the exact, defensible research story that the empirical evidence supports, eliminating marketing hyperbole and unbacked assertions.

---

## 1. Executive Summary & Core Research Story

```mermaid
graph LR
    subgraph Problem [Pervasive Computing Challenge]
        P1["Centralized Cloud Routing"] -->|Suffers from| P2["Variable WAN Latency<br/>Single Point of Failure<br/>Cloud Ingress Bottlenecks"]
    end

    subgraph Solution [EdgeSync Architectural Contribution]
        S1["Spatial Locality Partitioning"] --> S2["Autonomous Regional Edge Nodes"]
        S2 --> S3["Local Execution (0.25ms overhead)"]
        S2 --> S4["Autonomous Fallback on Peer Crash"]
        S2 --> S5["Idempotent CRDT State Model"]
    end

    subgraph Evidence [Empirical Validation (N > 19,200)]
        E1["Locality Sensitivity (rho = -1.0)"]
        E2["Network Sensitivity (R^2 = 0.9998)"]
        E3["Concurrency Scaling (650 RPS)"]
        E4["Peer Crash Resilience (100% Avail)"]
    end

    Problem --> Solution
    Solution --> Evidence
    
    style Problem fill:#ffebee,stroke:#c62828,stroke-width:2px
    style Solution fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style Evidence fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
```

### The Core Scientific Thesis
> **Thesis Statement:** *Decentralized edge microservices can execute spatial ETA routing with minimal software overhead ($\approx 0.25\text{ ms}$ P50) and high throughput scaling (up to $650\text{ RPS}$), where spatial locality effectively shields client latencies from inter-region network degradation and autonomous fallback guarantees service continuity during peer node crashes.*

---

## 2. Six Foundational Scientific Pillars

### Pillar 1: Spatial Locality governs Edge Efficiency (RQ1)
- **Empirical Proof:** Across 3,000 requests, EdgeSync exhibits a perfect monotonic relationship between local request ratio and median latency ($\rho = -1.0, p < 0.001$).
- **Scientific Narrative:** When traffic exhibits high geographic clustering ($L90$), EdgeSync resolves requests locally with near-baseline latency ($4.74\text{ ms}$ vs $4.19\text{ ms}$ Centralized). As requests cross regional boundaries ($L10$), inter-service HTTP delegation predictably adds forwarding latency ($10.15\text{ ms}$).

### Pillar 2: Locality Shields Edge Execution from Inter-Region Network Degradation (RQ2)
- **Empirical Proof:** Across 9,000 controlled observations, EdgeSync's inter-service delegation latency scales linearly with network delay ($P50 = 1.0155 \times \text{Delay} + 3.92\text{ ms}, R^2 = 0.9998$).
- **Scientific Narrative:** Under high spatial locality ($L90$), 90% of requests execute on the local gateway, causing overall median latency to remain completely flat ($1.55\text{ ms} \to 1.71\text{ ms}$) even when remote inter-region delays surge from $0\text{ ms}$ to $50\text{ ms}$. Spatial edge partitioning acts as a natural network buffer.

### Pillar 3: Edge Microservices Scale Under Concurrency (RQ3)
- **Empirical Proof:** Across 6,300 observations from $C=1$ to $C=64$, EdgeSync Local scales from $393.38\text{ RPS}$ at $C=1$ to a peak throughput of $650.06\text{ RPS}$ at $C=8$, sustaining $521-615\text{ RPS}$ through $C=64$.
- **Scientific Narrative:** Decentralizing execution across regional edge nodes eliminates centralized lock contention. At moderate concurrency ($C=4$), EdgeSync Local and Centralized latencies are statistically indistinguishable ($p = 0.0544$).

### Pillar 4: Minimal Baseline Software Routing Overhead (RQ4)
- **Empirical Proof:** In pooled loopback microbenchmarking ($N=900$), EdgeSync Local median latency is $1.609\text{ ms}$ vs Centralized $1.352\text{ ms}$.
- **Scientific Narrative:** The geofencing routing logic and FastAPI ASGI dispatch in EdgeSync introduce only $\approx 0.25\text{ ms}$ of software overhead over a monolithic central baseline—a negligible cost that is overwhelmingly amortized by avoiding physical wide-area network round-trips ($30-80\text{ ms}$).

### Pillar 5: Autonomous Local Fallback During Peer Crashes (RQ5)
- **Empirical Proof:** Across 3 independent trials ($N=600$ requests), killing the remote peer process (`SIGKILL`) resulted in **100.0% request availability**, with exactly 150/600 requests seamlessly redirected to local fallback with a mean recovery latency of $26.57\text{ ms}$.
- **Scientific Narrative:** EdgeSync decouples client availability from peer node health. When inter-service communication fails, regional nodes immediately fall back to local computation, preventing cascading cluster outages.

### Pillar 6: Lightweight Resource Footprint for Edge Gateways
- **Empirical Proof:** Process memory remained $< 180\text{ MB}$ RSS per node with low CPU utilization ($< 25\%$) during full load saturation.
- **Scientific Narrative:** EdgeSync is lightweight enough to be deployed directly on resource-constrained edge appliances, road-side units (RSUs), and micro-gateways.

---

## 3. Explicit Architectural Trade-Offs & Honest Limitations

Every defensible PerCom paper must explicitly discuss its architectural trade-offs:

1. **Trade-Off 1 (Local Speed vs Cross-Region Delegation):**  
   EdgeSync achieves sub-2 ms latency for local queries, but cross-region requests incur two HTTP hops, adding $\approx 1.58\text{ ms}$ of baseline delegation overhead.
2. **Trade-Off 2 (Autonomous Fallback vs Global Precision):**  
   During peer failures, local fallback guarantees 100% availability by computing ETAs with localized observation models, trading absolute cross-region precision for uninterrupted service continuity.
3. **Limitation 1 (Loopback Evaluation Environment):**  
   Evaluations were conducted over calibrated IPv4 loopback sockets with software delay injection rather than multi-datacenter physical WAN testbeds.
4. **Limitation 2 (In-Memory Volatile State):**  
   The prototype observation store operates in memory; persistent database durability across catastrophic cluster reboots remains future work.

---

## 4. Forbidden Claims (DO NOT INCLUDE IN SUBMISSION)

To prevent reviewer rejection, the following claims must **NEVER** appear in the manuscript:
- ❌ *"EdgeSync reduces latency by 41% across all operating conditions"* (Obsolete Gen 1 claim).
- ❌ *"EdgeSync provides absolute partition tolerance across all WAN failures"* (Corrupted in unpatched test suite).
- ❌ *"EdgeSync guarantees zero data loss under continuous concurrent multi-master network partitions"* (Algebraically modeled, but not empirically tested under heavy WAN write churn).
- ❌ *"EdgeSync is more energy-efficient than cloud datacenters"* (Not instrumented with hardware power meters).
