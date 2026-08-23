# EdgeSync Research Dossier: Master Research Index & Executive Assessment

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `16_MASTER_RESEARCH_INDEX.md`  
**Repository Analyzed:** `EdgeSync-ETA-main`

---

## 1. Executive Research Assessment (10 Core Questions Answered)

### Q1: What is the strongest part of EdgeSync?
**Answer:** The **regionally partitioned edge microservice architecture** ([`config.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/config.py), [`east.py`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py)). The concept of dividing a dense metropolitan city into spatial edge nodes that handle co-located spatial calculations locally and delegate cross-region legs via REST is clear, working, and highly relevant to urban pervasive computing.

### Q2: What is the weakest part of EdgeSync?
**Answer:** The **sample count inflation bug** in the gossip protocol ([`east.py:L120-L128`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L120-L128)) and the **total absence of quantitative experimental evaluation scripts**. The code currently lacks empirical latency benchmarks, load tests, or real-world accuracy validation.

### Q3: What is the strongest PerCom angle?
**Answer:** Positioning EdgeSync as an **"Urban Spatial Edge Computing Infrastructure"** that isolates localized traffic dynamics and co-located delivery queries at the regional edge while maintaining global statistical awareness through decentralized gossip protocols.

### Q4: What is currently preventing this from being a strong PerCom paper?
**Answer:** 
1. Overstated paper claims (e.g., claiming machine learning models and cloud proxy layers that are **NOT IMPLEMENTED**).
2. The mathematical flaw in gossip sample aggregation.
3. Lack of empirical experimental evaluation (latency CDFs, throughput scalability, fault recovery graphs).

### Q5: What are the top 5 experiments we should perform?
**Answer:**
1. *Latency Profiling:* Compare Intra-region vs. Cross-region vs. Centralized Cloud P95/P99 decision latency.
2. *Throughput & Scalability:* Measure maximum RPS under 10 to 1,000 concurrent client connections.
3. *Gossip Convergence:* Plot state divergence $|A_E - A_W|$ over time after a traffic spike.
4. *Fault Recovery:* Measure request success rate and recovery time when a regional node crashes.
5. *Network Control Overhead:* Quantify gossip payload overhead (bytes/sec) vs. data payload traffic.

### Q6: What are the top 5 implementation improvements?
**Answer:**
1. *Fix Gossip Idempotency:* Replace raw sample addition in `sync()` with timestamped windowed aggregation vectors.
2. *Fix Food Prep Bug:* Normalize string input `food.lower()` in `utils.get_prep_time` to match lowercase dictionary keys.
3. *Add Exception Handling:* Wrap cross-region REST calls in `custom_eta()` with `try-except` blocks and HTTP timeouts.
4. *Embed Edge ML Inference:* Train a lightweight LightGBM / ONNX model to replace static speed heuristics.
5. *Dynamic Configuration:* Replace hardcoded `localhost` URLs with environment variables (`os.getenv`).

### Q7: What claims in the current paper are risky?
**Answer:**
- Claiming LightGBM / Machine Learning models exist (**NOT IMPLEMENTED**).
- Claiming a stateless cloud coordination proxy layer exists (**NOT IMPLEMENTED**).
- Claiming gossip merge is idempotent and prevents double-counting (**FALSE IN CODE**).
- Claiming 60-95% latency reduction without empirical measurement files (**UNBACKED**).

### Q8: What claims are strongly supported?
**Answer:**
- Geographic partitioning of Mumbai into East, West, and Central regions.
- Haversine distance travel time calculations.
- Discrete dynamic traffic speed modeling (15, 25, 35 km/h).
- Unidirectional background gossip ring execution.
- Interactive Streamlit frontend visualization.

### Q9: What information is missing from the repository?
**Answer:** Real-world GPS trajectory datasets, live traffic sensor feeds, automated benchmark test scripts, Docker containerization manifests, and baseline comparison code.

### Q10: What should be prioritized before submission?
**Answer:**
1. **Phase 1 (Week 1):** Fix the gossip sample bug and food prep bug in source code.
2. **Phase 2 (Week 2):** Build the automated benchmark harness (`experiments/run_benchmarks.py`) and collect empirical evaluation data.
3. **Phase 3 (Week 3-4):** Embed a trained ONNX model for edge ETA prediction and update paper text to accurately reflect code reality.

---

## 2. Dossier Master Index

| File Name | Document Title | Description & Core Focus |
| :--- | :--- | :--- |
| [`00_PROJECT_OVERVIEW.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/00_PROJECT_OVERVIEW.md) | Project Overview | Summary of EdgeSync, problem statement, core idea, tech stack, repository tree, and maturity assessment. |
| [`01_ARCHITECTURE_DEEP_DIVE.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/01_ARCHITECTURE_DEEP_DIVE.md) | Architecture Deep Dive | Microservice layers, regional configurations, end-to-end request lifecycles, and Mermaid diagrams. |
| [`02_API_AND_MICROSERVICE_ANALYSIS.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/02_API_AND_MICROSERVICE_ANALYSIS.md) | API & Microservice Analysis | Detailed specs for `/custom_eta`, `/calc_delivery`, `/sync`, `/logs` across all nodes. |
| [`03_ETA_MODEL_DEEP_ANALYSIS.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/03_ETA_MODEL_DEEP_ANALYSIS.md) | ETA Model Deep Analysis | Reverse-engineering of Haversine distance, speed map, prep time, rider distance, case-sensitivity bug, and math formulas. |
| [`04_GOSSIP_PROTOCOL_ANALYSIS.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/04_GOSSIP_PROTOCOL_ANALYSIS.md) | Gossip Protocol Analysis | Unidirectional ring topology, 5s tick, sample-weighted merge formula, sample inflation bug, and fault tolerance. |
| [`05_EDGE_COMPUTING_AND_PERCOM_RELEVANCE.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/05_EDGE_COMPUTING_AND_PERCOM_RELEVANCE.md) | PerCom Relevance Analysis | Locality, spatio-temporal awareness, distributed intelligence, and PerCom topic mapping matrix. |
| [`06_IMPLEMENTATION_VS_PAPER.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/06_IMPLEMENTATION_VS_PAPER.md) | Implementation vs Paper | Comprehensive audit table matching paper claims in `EdgeSyncETA_Final.doc` against Python code evidence. |
| [`07_EXPERIMENTAL_EVALUATION_GAP_ANALYSIS.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/07_EXPERIMENTAL_EVALUATION_GAP_ANALYSIS.md) | Evaluation Gap Analysis | Detailed blueprint for 9 PerCom experiments (Latency, Throughput, Gossip Convergence, Fault Tolerance, etc.). |
| [`08_BASELINES_AND_COMPARISON_DESIGN.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/08_BASELINES_AND_COMPARISON_DESIGN.md) | Baselines Comparison Design | Specifications for 5 comparison baselines (Centralized, Hybrid Edge-Cloud, No Gossip, No Partitioning, Var Gossip Freq). |
| [`09_ABLATION_STUDY_DESIGN.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/09_ABLATION_STUDY_DESIGN.md) | Ablation Study Design | Design of 7 ablation studies isolating partitioning, delegation, gossip, traffic model, prep noise, and rider proximity. |
| [`10_REPRODUCIBILITY_GUIDE.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/10_REPRODUCIBILITY_GUIDE.md) | Reproducibility Guide | Installation commands, server startup instructions, curl test suite, parameter configuration, and gotchas. |
| [`11_RESEARCH_LIMITATIONS.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/11_RESEARCH_LIMITATIONS.md) | Research Limitations | Categorized technical, architectural, gossip, model, and dataset limitations with priority fix recommendations. |
| [`12_PERCOM_RESEARCH_OPPORTUNITIES.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/12_PERCOM_RESEARCH_OPPORTUNITIES.md) | PerCom Research Opportunities | Ranked research opportunities (Adaptive Partitioning, Edge ML, Dynamic Gossip, Uncertainty Bounds) with effort estimates. |
| [`13_POTENTIAL_RESEARCH_CONTRIBUTIONS.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/13_POTENTIAL_RESEARCH_CONTRIBUTIONS.md) | Potential Contributions | Novelty claims categorized by 4 readiness tiers with reviewer rejection risk assessments. |
| [`14_RECOMMENDED_PAPER_STRUCTURE.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/14_RECOMMENDED_PAPER_STRUCTURE.md) | Recommended Paper Structure | Proposed 14-section IEEE PerCom 8-page paper outline mapping existing code evidence and required data. |
| [`15_EXPERIMENT_EXECUTION_CHECKLIST.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/15_EXPERIMENT_EXECUTION_CHECKLIST.md) | Experiment Execution Checklist | Markdown checkbox checklist organized by Critical, Strongly Recommended, and Optional priorities. |
| [`17_INSTRUMENTATION_POINTS.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/17_INSTRUMENTATION_POINTS.md) | Code Instrumentation Points | Code file, function, and line-level instructions for inserting timing hooks, latency counters, and network meters. |
| [`18_DATA_AND_DATASET_ANALYSIS.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/18_DATA_AND_DATASET_ANALYSIS.md) | Data & Dataset Analysis | Audit of existing repository data, data gap assessment, and requirements for real-world benchmarks. |
| [`19_RECOMMENDED_FIGURES_AND_TABLES.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/19_RECOMMENDED_FIGURES_AND_TABLES.md) | Recommended Figures & Tables | Detailed specifications for 14 key figures and tables required in the final IEEE PerCom paper. |
| [`20_FINAL_GAP_SUMMARY.md`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/research_docs/20_FINAL_GAP_SUMMARY.md) | Final Gap Summary | Concise executive synthesis of current state, scientific fit, weaknesses, missing work, and prioritized action plan. |
