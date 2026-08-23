# EdgeSync Research Dossier: Recommended Figures & Tables

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `19_RECOMMENDED_FIGURES_AND_TABLES.md`

---

## 1. Specifications for Final Paper Figures & Tables

To present a compelling systems paper for IEEE PerCom 2027, the manuscript should feature **14 vector-quality figures and structured tables**. This document specifies the title, axes, data inputs, experimental source, and target research question for each element.

---

## 2. Complete Figures & Tables Catalog

### Figure 1: EdgeSync Overall Distributed System Architecture
- **Type:** Conceptual Architecture Diagram
- **Content:** Illustrates 3 regional edge clusters (`EAST`, `WEST`, `CENTRAL`), client interaction, REST inter-node delegation lines, and background gossip ring.
- **Research Question Answered:** How are regional edge microservices partitioned and connected across the urban delivery ecosystem?

---

### Figure 2: End-to-End Request Lifecycle Sequence Diagram
- **Type:** UML Sequence Diagram
- **Content:** Sequence flow between User $\rightarrow$ Streamlit UI $\rightarrow$ Source Node $\rightarrow$ Destination Node $\rightarrow$ Response.
- **Research Question Answered:** How does EdgeSync handle cross-region delegation versus local processing?

---

### Figure 3: Geographic Edge Partitioning Map of Mumbai
- **Type:** Geospatial Coordinate Map
- **Content:** Folium/QGIS map of Mumbai overlaying coordinate boundaries ($19.05^\circ\text{N}$, $72.85^\circ\text{E}$) dividing Central, West, and East zones.
- **Research Question Answered:** How does spatial geometry define regional edge compute domains?

---

### Figure 4: Gossip Synchronization Ring Topology
- **Type:** Directed Graph Diagram
- **Content:** 3-node ring topology ($E \rightarrow W \rightarrow C \rightarrow E$) detailing `/sync` REST payloads and 5-second tick interval.

---

### Figure 5: ETA Computation Pipeline Flowchart
- **Type:** Block Diagram
- **Content:** Algorithmic flowchart showing Haversine math, speed lookup, rider pickup sampling, prep time sampling, and $\max(\text{pickup}, \text{prep}) + \text{delivery}$ aggregation.

---

### Figure 6: Cumulative Distribution Function (CDF) of Decision Latency
- **Type:** Line Plot (Vector PDF)
- **X-axis:** Response Latency (milliseconds)
- **Y-axis:** Cumulative Probability $P(X \le x)$
- **Data Required:** 10,000 latency measurements across (1) Intra-region EdgeSync, (2) Cross-region EdgeSync, (3) Centralized Cloud Baseline.
- **Experiment Source:** Experiment A ([`07_EXPERIMENTAL_EVALUATION_GAP_ANALYSIS.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/07_EXPERIMENTAL_EVALUATION_GAP_ANALYSIS.md)).
- **Research Question Answered:** Does regional edge processing reduce decision latency compared to centralized cloud routing?

---

### Figure 7: P95 and P99 Latency under Increasing Concurrency
- **Type:** Grouped Bar Chart / Line Plot
- **X-axis:** Concurrent Client Connections $C \in \{10, 50, 100, 500, 1000\}$
- **Y-axis:** P95 & P99 Latency (milliseconds)
- **Data Required:** Benchmark latency logs from Experiment E.
- **Research Question Answered:** How does decision latency scale under high concurrent request loads?

---

### Figure 8: System Throughput Capacity
- **Type:** Line Plot
- **X-axis:** Target Request Rate (Requests/sec)
- **Y-axis:** Actual Throughput (RPS) & HTTP Error Rate (%)
- **Research Question Answered:** What is the maximum throughput capacity of the EdgeSync microservice cluster?

---

### Figure 9: Gossip State Convergence & Divergence Over Time
- **Type:** Multi-Line Time Series
- **X-axis:** Time (seconds)
- **Y-axis:** Running Average ETA `avg_eta` (minutes)
- **Lines Plotted:** EAST Node, WEST Node, CENTRAL Node
- **Data Required:** Time-stamped state logs after injecting a traffic spike into EAST node.
- **Experiment Source:** Experiment C.
- **Research Question Answered:** How fast does decentralized gossip propagate state changes across regional edge nodes?

---

### Figure 10: Fault Tolerance & Recovery Timeline
- **Type:** Timeline / Area Plot
- **X-axis:** Elapsed Time (seconds)
- **Y-axis:** Successful HTTP Responses (200 OK) / Failed Requests (500 Error)
- **Event Annotations:** $t=30\text{s}$ (WEST node killed), $t=60\text{s}$ (WEST node restarted).
- **Experiment Source:** Experiment D.
- **Research Question Answered:** How resilient is EdgeSync to regional node outages?

---

### Figure 11: Edge Node Resource Utilization (CPU & RAM)
- **Type:** Dual-Y Axis Time Series Plot
- **X-axis:** Time (minutes)
- **Y1-axis (Left):** CPU Utilization (%)
- **Y2-axis (Right):** Memory Footprint RSS (MB)
- **Experiment Source:** Experiment H.

---

### Figure 12: Cross-Region Delegation Overhead Breakdown
- **Type:** Stacked Bar Chart
- **X-axis:** Request Type (Intra-Region vs Cross-Region)
- **Y-axis:** Time Breakdown (ms): Local Math + Network Transmission + Remote Computation.

---

### Figure 13: ETA Sensitivity to Distance & Traffic Levels
- **Type:** Grouped Bar Chart
- **X-axis:** Travel Distance (1 km, 5 km, 10 km, 20 km)
- **Y-axis:** Estimated Delivery Time (minutes)
- **Bars:** Low (35 km/h), Medium (25 km/h), High (15 km/h) traffic.

---

### Table 14: Master Ablation Comparison Table
- **Type:** Structured Markdown / LaTeX Table
- **Columns:** Ablation Variant, P50 Latency (ms), P95 Latency (ms), Throughput (RPS), State Divergence $\Delta A$, Accuracy MAE (mins).
- **Experiment Source:** Ablation Studies ([`09_ABLATION_STUDY_DESIGN.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/09_ABLATION_STUDY_DESIGN.md)).
