# EdgeSync Research Dossier: Implementation vs. Paper Comparison

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `06_IMPLEMENTATION_VS_PAPER.md`

---

## 1. Executive Summary of Discrepancies

A comprehensive line-by-line audit comparing the existing research manuscript (`EdgeSyncETA_Final.doc`) against the Python source code repository (`EdgeSync-ETA-main`) revealed major discrepancies across machine learning claims, cloud coordination infrastructure, gossip protocol mathematical properties, and experimental evaluation.

---

## 2. Master Paper Claim vs. Implementation Audit Table

| # | Paper Claim | Actual Implementation | Code Evidence | Status | Required Paper Correction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | *"EdgeSync combines machine learning models, edge computing, and lightweight algorithms."* | Purely deterministic Haversine distance formula with speed lookups. No ML models used. | [`utils.py:L6-L28`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L6-L28) | **NOT IMPLEMENTED** | Remove claims of using ML models in current implementation; reframe as "architectural framework capable of hosting future edge ML models". |
| **2** | *"Lightweight cloud coordinating layer acts as entry point and routes delivery requests."* | Streamlit UI imports `get_region` directly and calls regional ports directly. No cloud service exists. | [`ui.py:L9`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/ui.py#L9), [`ui.py:L116-L129`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/ui.py#L116-L129) | **NOT IMPLEMENTED** | Clarify that UI performs client-side regional lookup and directly invokes regional edge endpoints. |
| **3** | *"Gossip merge function is idempotent with respect to repeated merges, preventing double-counting."* | `sync()` adds incoming `samples` to local `samples` unconditionally on every 5s tick. | [`east.py:L120-L128`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L120-L128) | **OVERSTATED / FALSE** | Fix code implementation to support vector clocks or timestamped sample counts, or retract idempotency claim in paper. |
| **4** | *"Microservices for Rider Distance, Restaurant Prep, Traffic Analysis, and ETA Aggregation."* | Inline function calls in monolithic `/custom_eta` endpoint. No individual microservices for sub-tasks. | [`east.py:L19-L74`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L19-L74) | **PARTIALLY ACCURATE** | Rephrase as "modular internal functions within each regional microservice node". |
| **5** | *"60–95% latency reduction compared to centralized cloud computing."* | Citation of external literature ([6]), but no latency benchmark scripts or empirical tests in repo. | Entire repository search (0 benchmark files) | **IMPLEMENTED BUT NOT QUANTITATIVELY EVALUATED** | Explicitly label as literature-based motivation; design and run local vs. cloud latency experiments before submission. |
| **6** | *"High fault tolerance and high scalability across regional nodes."* | Try-except in background gossip thread, but cross-region `/calc_delivery` calls lack error handling. | [`east.py:L52-L56`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L52-L56) | **PARTIALLY ACCURATE** | Add try-except and timeout logic to cross-region HTTP calls; conduct empirical node crash experiments. |
| **7** | *"Geographic partitioning into East, West, and Central clusters."* | Implemented via coordinate threshold checks (`lat < 19.05`, `lon < 72.85`). | [`config.py:L1-L7`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/config.py#L1-L7) | **ACCURATE** | Matches implementation. |
| **8** | *"Haversine distance and speed-based time estimation."* | Implemented in `utils.distance` ($R=6371\text{ km}$) and `utils.estimate_time_from_distance`. | [`utils.py:L6-L28`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L6-L28) | **ACCURATE** | Matches implementation. |
| **9** | *"ETA = max(Pickup, Prep) + Delivery formula."* | Implemented exactly as formula states. | [`east.py:L60`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L60) | **ACCURATE** | Matches implementation. |
| **10** | *"Stochastic perturbation on rider distance and food prep time."* | Implemented via `random.uniform(0.9, 1.1)`. | [`utils.py:L50, L62`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L50-L62) | **ACCURATE** | Note food case-sensitivity bug in paper notes. |
| **11** | *"Unidirectional gossip ring topology (East -> West -> Central -> East)."* | Implemented via background threads sending HTTP POST requests every 5 seconds. | [`east.py:L102`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L102), [`west.py:L102`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/west.py#L102), [`central.py:L102`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/central.py#L102) | **ACCURATE** | Matches implementation. |
| **12** | *"Interactive Streamlit interface with Folium map for real-time simulation."* | Implemented in `ui.py` with 2-point click selection and Matplotlib chart rendering. | [`ui.py:L1-L197`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/ui.py#L1-L197) | **ACCURATE** | Matches implementation. |

---

## 3. Recommended Actions Before PerCom Submission

1. **Remove / Reframe ML Claims:** Do not present the current prototype as a machine learning system. Position EdgeSync as an **edge architecture and distributed synchronization platform for urban spatial services**.
2. **Correct Idempotency Description:** Either fix the `sync()` algorithm in code or update the paper text to describe best-effort aggregation.
3. **Execute Quantitative Experiments:** Conduct formal benchmarking to replace qualitative claims with empirical graphs and tables.
