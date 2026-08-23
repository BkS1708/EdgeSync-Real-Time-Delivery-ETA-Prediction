# EdgeSync Research Dossier: PerCom Research Opportunities

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `12_PERCOM_RESEARCH_OPPORTUNITIES.md`

---

## 1. Executive Research Strategy for PerCom 2027

To elevate EdgeSync from a basic simulation prototype into a competitive IEEE PerCom 2027 paper, we identify **5 high-impact research opportunities**. These opportunities address fundamental pervasive computing challenges: spatial dynamic partitioning, edge ML inference, adaptive gossip protocols, uncertainty quantification, and resilient distributed routing.

---

## 2. Detailed Research Opportunity Profiles

### Opportunity 1: Adaptive Spatio-Temporal Geographic Partitioning
- **Rank:** **CRITICAL**
- **Research Problem:** Static coordinate partitioning (`lat < 19.05`, `lon < 72.85`) leads to severe workload imbalances when delivery density shifts dynamically during peak hours (e.g., heavy lunch traffic in Central vs. dinner traffic in West).
- **Proposed Improvement:** Implement a dynamic Voronoi or Quadtree spatial partitioning algorithm where edge cluster boundaries adapt dynamically based on real-time request volume and regional traffic congestion.
- **Why PerCom Cares:** Direct relevance to *Adaptive Pervasive Systems*, *Mobile Data Management*, and *Spatial Computing*.
- **Required Implementation:** A lightweight spatial boundary coordinator algorithm that re-balances boundary thresholds every 15 minutes based on load telemetry.
- **Required Experiment:** Compare static vs. dynamic partitioning under uneven regional request distributions; measure cross-region hop reduction and node CPU balance.
- **Expected Contribution:** First dynamic spatial partitioning algorithm tailored for urban edge ETA microservices.
- **Difficulty / Effort:** High (Estimated 2-3 weeks).

---

### Opportunity 2: Decentralized Edge ML Inference Engine
- **Rank:** **HIGH**
- **Research Problem:** Pure heuristic speed equations fail to capture complex non-linear spatial interactions, weather delays, and multi-hop routing bottlenecks.
- **Proposed Improvement:** Replace static Haversine speed mapping with ONNX runtime executing lightweight LightGBM / XGBoost decision trees pre-trained on open urban delivery trajectory datasets.
- **Why PerCom Cares:** Aligns with *Edge AI*, *Ubiquitous Intelligence*, and *Real-Time Pervasive Analytics*.
- **Required Implementation:** Train LightGBM model on OpenStreetMap / Uber Movement data; embed `.onnx` inference engine inside FastAPI `/custom_eta` endpoints.
- **Required Experiment:** Benchmark prediction accuracy (MAE, RMSE, MAPE) against baseline heuristics; measure inference latency on edge nodes (target < 5ms).
- **Expected Contribution:** Proof of real-time edge ML inference accuracy vs cloud round-trip delay.
- **Difficulty / Effort:** Medium (Estimated 1-2 weeks).

---

### Opportunity 3: Workload-Aware Dynamic Gossip Synchronization
- **Rank:** **HIGH**
- **Research Problem:** Fixed 5-second gossip ticks cause unnecessary network overhead during idle hours and state lag during sudden traffic bursts.
- **Proposed Improvement:** Implement an adaptive gossip protocol that adjusts tick frequency $\Delta t \in [1\text{s}, 30\text{s}]$ dynamically based on local request rate ($\frac{dN}{dt}$) and state variance ($\Delta A$).
- **Why PerCom Cares:** Core contribution to *Pervasive Communication Protocols* and *Distributed Energy/Bandwidth Optimization*.
- **Required Implementation:** Update `gossip()` loop to compute tick sleep dynamically: $\Delta t = \max(1, \min(30, \frac{\alpha}{\Delta A}))$.
- **Required Experiment:** Plot network bandwidth overhead (bytes/sec) vs state convergence delay across static vs adaptive gossip intervals.
- **Expected Contribution:** Reduction of control message overhead by 40-60% without sacrificing state convergence accuracy.
- **Difficulty / Effort:** Medium (Estimated 1 week).

---

### Opportunity 4: Uncertainty-Aware ETA Prediction & Confidence Intervals
- **Rank:** **MEDIUM**
- **Research Problem:** Point estimates ($\text{ETA} = 28.5\text{ mins}$) fail to convey predictive uncertainty under volatile traffic conditions.
- **Proposed Improvement:** Output quantile predictions (e.g. 10th, 50th, 90th percentiles) representing confidence bounds $[\text{ETA}_{\text{min}}, \text{ETA}_{\text{max}}]$.
- **Why PerCom Cares:** Advances *Context-Aware Systems* and *Human-Centric Pervasive Computing*.
- **Required Implementation:** Implement quantile regression trees in edge ML engine.
- **Difficulty / Effort:** Medium (Estimated 1 week).

---

### Opportunity 5: Resilient Cross-Region Circuit Breakers
- **Rank:** **MEDIUM**
- **Research Problem:** Network failures between regional nodes block cross-region ETA calculations.
- **Proposed Improvement:** Add fallback local estimation + exponential backoff circuit breaker for peer REST requests.
- **Why PerCom Cares:** *Fault-Tolerant Distributed Infrastructures*.
- **Difficulty / Effort:** Low (Estimated 3-5 days).
