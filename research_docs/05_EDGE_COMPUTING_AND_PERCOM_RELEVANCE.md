# EdgeSync Research Dossier: Edge Computing & PerCom Relevance

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `05_EDGE_COMPUTING_AND_PERCOM_RELEVANCE.md`

---

## 1. Positioning EdgeSync in Pervasive Systems Research

IEEE PerCom is the premier conference on pervasive computing and communications. Systems submitted to PerCom are evaluated on system design, distributed infrastructure, context-awareness, spatio-temporal intelligence, real-time responsiveness, and empirical systems evaluation.

EdgeSync aligns with the core domain of **Urban Pervasive Computing & Smart Logistics Infrastructure**.

---

## 2. Analysis of Edge Computing Characteristics in Code

### A. Spatial Locality & Geographic Bounding
The system enforces spatial partitioning by mapping physical coordinates directly to localized microservice boundaries.
- **Code Evidence:** [`config.py:L1-L7`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/config.py#L1-L7) (`get_region(lat, lon)`).
- **Edge Value:** Computations for orders originating in powders like Powai or Bandra are retained within the local regional microservice stack rather than being transmitted to a distant centralized cloud.

### B. Distributed Computation & Microservice Isolation
Instead of a monolithic cloud service, processing is distributed across three autonomous nodes (`east.py`, `west.py`, `central.py`).
- **Code Evidence:** Independent FastAPI apps listening on ports `8000`, `9000`, `10000`.
- **Edge Value:** Decreases core network hop counts for intra-region requests and isolates compute load across geographic zones.

### C. Spatio-Temporal Context Awareness
The system integrates spatial coordinates (latitude, longitude) with temporal context (time of day) to compute dynamic ETAs.
- **Code Evidence:** [`utils.py:L31-L39`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L31-L39) (`dynamic_traffic()`).
- **Edge Value:** Real-time situational awareness (peak morning/evening traffic vs off-peak hours) adjusts travel speed dynamically.

---

## 3. IEEE PerCom Topic Alignment Matrix

| PerCom Track / Topic | EdgeSync System Component | Source Code Evidence | System Alignment Strength |
| :--- | :--- | :--- | :--- |
| **Edge & Fog Computing** | Regional microservices (`EAST`, `WEST`, `CENTRAL`) running on independent ports. | [`east.py:L8`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#8), [`west.py:L8`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/west.py#L8), [`central.py:L8`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/central.py#L8) | **HIGH** |
| **Spatio-Temporal Data Systems** | Spatial partitioning via Haversine geometry and time-of-day traffic mapping. | [`config.py:L1-L7`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/config.py#L1-L7), [`utils.py:L6-L39`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L6-L39) | **HIGH** |
| **Mobile & Urban Intelligence** | Real-time ETA prediction for metropolitan food delivery across Mumbai zones. | [`ui.py:L27`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/ui.py#L27) (Map location `[19.0760, 72.8777]`) | **HIGH** |
| **Distributed Systems Protocols** | Peer-to-peer gossip ring synchronization for regional ETA statistics. | [`east.py:L98-L132`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L98-L132) | **MEDIUM** *(Weakened by sample inflation bug)* |
| **Pervasive Data Management** | Volatile in-memory sample-weighted aggregation. | [`east.py:L13-L16`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L13-L16) | **LOW** *(No persistent storage or DB)* |
| **Adaptive & Resilient Systems** | Background thread retry on network failure. | [`east.py:L105-L106`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L105-L106) | **LOW** *(Cross-region calls lack fault tolerance)* |
| **Edge ML / Decentralized AI** | Machine learning inference at the edge. | **None** | **NOT IMPLEMENTED** *(Purely formula-based)* |

---

## 4. Key Gaps to Address for PerCom Submission

1. **Lack of Hardware Realism:** Currently run as local Python processes on `localhost`. PerCom expects evaluation on actual distributed hardware (e.g., Raspberry Pis, NVIDIA Jetson edge nodes, or multi-region AWS/GCP instances).
2. **Missing Real-World Sensors:** Traffic is currently modeled by system clock hour lookup rather than live IoT traffic sensor feeds or GPS streams.
3. **Missing Empirical Evaluation:** PerCom requires rigorous quantitative benchmarking (latency CDFs, network payload overheads, throughput under concurrency, and failure recovery times).
