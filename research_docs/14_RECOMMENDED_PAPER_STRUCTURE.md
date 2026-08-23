# EdgeSync Research Dossier: Recommended IEEE PerCom 2027 Paper Structure

**Target Conference:** IEEE PerCom 2027 (8-Page Double-Column IEEE Format)  
**Document ID:** `14_RECOMMENDED_PAPER_STRUCTURE.md`

---

## 1. Proposed Paper Title

**"EdgeSync: A Regionally-Partitioned Edge Microservice Framework with Gossip Synchronization for Real-Time Urban Delivery ETA Prediction"**

---

## 2. Section-by-Section Structural Breakdown

### Section I: Introduction (Page 1)
- **Content:** Growth of metropolitan food delivery platforms, severe traffic fluctuations (e.g. Mumbai), latency and single-point-of-failure vulnerabilities of centralized cloud systems. Core thesis of EdgeSync.
- **Existing Evidence:** Project background in [`README.md:L7-L23`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/README.md#L7-L23) and `EdgeSyncETA_Final.doc`.
- **New Evidence Needed:** Citations of 2025/2026 urban delivery latency benchmarks.

---

### Section II: Related Work & Background (Page 2)
- **Content:** Survey across 3 domains: (1) Machine Learning for ETA prediction (LightGBM, GNNs); (2) Edge Computing for Smart Transportation; (3) Gossip Protocols for Pervasive Systems. Positioning of EdgeSync.
- **Existing Evidence:** Table I literature survey in `EdgeSyncETA_Final.doc`.
- **New Evidence Needed:** Expanded comparison matrix distinguishing EdgeSync from cloud-only and static edge models.

---

### Section III: Problem Formulation & System Model (Page 2.5)
- **Content:** Mathematical formulation of geographic space $\mathcal{S} \subset \mathbb{R}^2$, region partition $\mathcal{S} = \bigcup_{i=1}^N \mathcal{R}_i$, ETA component decomposition: $\text{ETA} = \max(T_{\text{pickup}}, T_{\text{prep}}) + T_{\text{delivery}}$.
- **Existing Evidence:** Core math in [`utils.py:L6-L28`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L6-L28) and [`east.py:L60`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L60).
- **New Evidence Needed:** Formal definitions of region boundary functions $\mathcal{B}(\text{lat}, \text{lon})$.

---

### Section IV: EdgeSync Distributed System Architecture (Page 3-4)
- **Content:** Architectural breakdown of regional edge clusters (`EAST`, `WEST`, `CENTRAL`), microservice API stack (`/custom_eta`, `/calc_delivery`), and inter-node REST communication protocol.
- **Existing Evidence:** Microservice code in [`east.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py), [`west.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/west.py), [`central.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/central.py).
- **New Evidence Needed:** Mermaid/Visio high-resolution architectural diagram showing edge microservices and gossip ring.

---

### Section V: Decentralized Gossip Synchronization Protocol (Page 4-5)
- **Content:** Ring topology specification, 5-second tick interval, sample-weighted state aggregation algorithm, and eventual consistency properties.
- **Existing Evidence:** Gossip loop and `/sync` endpoint in [`east.py:L98-L132`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L98-L132).
- **New Evidence Needed:** Proof/fix of idempotency using timestamped windowed vectors to prevent sample count inflation.

---

### Section VI: Experimental Setup & Methodology (Page 5-6)
- **Content:** Hardware testbed (e.g. 3 edge nodes + 1 client node), load generation parameters, evaluation metrics (Latency P50/P95/P99, RPS, control overhead, recovery time).
- **Existing Evidence:** None (**`IMPLEMENTED BUT NOT QUANTITATIVELY EVALUATED`**).
- **New Evidence Needed:** Execution logs from `experiments/run_benchmarks.py`.

---

### Section VII: Performance Evaluation & Discussion (Page 6-7.5)
- **Content:** Results from Experiments A through I: Latency CDFs, throughput scalability graphs, gossip convergence curves, fault tolerance failure/recovery timelines.
- **Existing Evidence:** None.
- **New Evidence Needed:** Generated Matplotlib/Seaborn vector graphs (.pdf format).

---

### Section VIII: Ablation Studies (Page 7.5)
- **Content:** Quantitative impact of removing partitioning, cross-region delegation, gossip, or dynamic traffic models.
- **Existing Evidence:** None.
- **New Evidence Needed:** Ablation summary table comparing full system vs. ablated variants.

---

### Section IX: Conclusion & Future Directions (Page 8)
- **Content:** Summary of contributions, key findings, limitations, and future work (dynamic partitioning, edge ML inference).
