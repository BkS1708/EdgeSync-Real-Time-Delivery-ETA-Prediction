# EdgeSync Research Dossier: Baselines & Comparison Design

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `08_BASELINES_AND_COMPARISON_DESIGN.md`

---

## 1. Rationale for Comparative Evaluation

To prove the systems contribution of EdgeSync for IEEE PerCom 2027, the proposed architecture must be empirically evaluated against established architectural paradigms. This document designs **5 scientifically rigorous baselines**.

---

## 2. Master Baseline Specification Matrix

| Baseline Name | Architectural Description | What Changes vs EdgeSync | What Remains Identical | Target Metric Tested | Scientific Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline 1: Centralized Cloud** | Single monolithic server process handling all Mumbai requests. | No regional nodes; single server on port 8000. All requests sent to 1 URL. | Haversine distance, speed model, pickup/prep formulas. | Network latency, central server CPU load, single-point failure impact. | Represents current industry standard cloud deployment (e.g. Swiggy/Zomato central cloud backend). |
| **Baseline 2: Hybrid Edge-Cloud** | Edge handles local pickup/prep; global cloud server computes delivery travel leg. | Pickup/prep computed on local edge node; delivery request sent to central cloud server. | Math formulas, spatial coordinates. | Inter-service network hops, cloud traffic volume, hybrid processing latency. | Evaluates conventional hybrid edge-cloud offloading architecture. |
| **Baseline 3: EdgeSync w/o Gossip** | Regional edge microservices w/ cross-region REST, but gossip protocol disabled. | Gossip background thread turned off (`gossip()` disabled). | Microservices, spatial partitioning, REST delegation. | Impact of gossip on global state awareness and convergence. | Measures the specific performance and consistency contribution of the gossip layer. |
| **Baseline 4: EdgeSync w/o Partitioning** | Local edge node processing all regions without geographic spatial partitioning. | `config.get_region` bypassed; single regional node processes all spatial coordinates. | Microservice code structure. | Spatial locality benefit, compute load distribution. | Tests whether geographic partitioning provides measurable latency/isolation benefits. |
| **Baseline 5: Var Gossip Freq** | EdgeSync ring w/ gossip intervals $\Delta t \in \{1\text{s}, 5\text{s}, 10\text{s}, 30\text{s}, 60\text{s}\}$. | `time.sleep(5)` replaced with configurable parameter $\Delta t$. | All microservice and gossip logic. | Tradeoff between network bandwidth overhead and state convergence time. | Determines optimal gossip tick frequency for urban edge deployments. |

---

## 3. Implementation Blueprint for Baselines

To construct these baselines for experimental execution:
1. **Centralized Baseline Script (`baselines/centralized_cloud.py`):**
   Combine `east.py` logic into a single FastAPI app listening on port 8000. Route all requests directly without checking `get_region`.
2. **Hybrid Baseline Script (`baselines/hybrid_edge_cloud.py`):**
   Deploy 3 local edge nodes for pickup/prep, plus 1 cloud server on port 7000 for delivery calculations.
3. **Gossip Toggle Flag:**
   Add command-line flag `--disable-gossip` to microservice startup commands.
