# EdgeSync Research Dossier: Final Research & Implementation Gap Summary

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `20_FINAL_GAP_SUMMARY.md`  
**Completion Date:** August 2026

---

## 1. Executive Synthesis of Current System State

| Dimension | Assessment & Current Reality in Codebase |
| :--- | :--- |
| **Current System State** | A working Python **Proof-of-Concept (PoC)** prototype implementing 3 FastAPI microservice nodes (`east.py`, `west.py`, `central.py`) for Mumbai spatial partitioning, cross-region REST delegation, a 5-second background gossip thread, and a Streamlit UI (`ui.py`). |
| **Current Scientific Contribution** | A regionally partitioned edge microservice architecture that isolates localized urban delivery queries while maintaining decentralized state awareness across node boundaries. |
| **Current PerCom Fit** | **MODERATE** in current state; has potential to be **VERY HIGH** once gossip sample inflation is fixed, edge ML inference is embedded, and quantitative latency/scalability benchmarks are executed. |
| **Biggest Weakness** | (1) Total lack of empirical measurement scripts or benchmarking data; (2) Sample count inflation bug in gossip aggregation algorithm. |

---

## 2. Claim Classification Audit

### Strong Claims (Supported by Code Base)
- Geographic spatial coordinate partitioning into East, West, and Central Mumbai zones ([`config.py:L1-L7`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/config.py#L1-L7)).
- Haversine distance travel time computation ($R=6371\text{ km}$) ([`utils.py:L6-L17`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L6-L17)).
- $\text{ETA} = \max(\text{pickup}, \text{prep}) + \text{delivery}$ aggregation ([`east.py:L60`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L60)).
- Interactive Folium map click-based frontend UI ([`ui.py:L27-L61`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/ui.py#L27-L61)).

### Risky Claims (Must be Corrected or Implemented)
- **Machine Learning Inference:** Claims of LightGBM / ML ETA models (**`NOT IMPLEMENTED`** in code).
- **Stateless Cloud Proxy Layer:** Claims of a standalone cloud routing service (**`NOT IMPLEMENTED`**).
- **Gossip Idempotency:** Claims that gossip merge prevents double-counting (**`FALSE IN CODE`** due to sample count inflation).
- **60-95% Latency Reduction:** Unbacked quantitative claim (**`IMPLEMENTED BUT NOT QUANTITATIVELY EVALUATED`**).

---

## 3. Prioritized Action Plan for IEEE PerCom 2027 Submission

```mermaid
graph LR
    P1["Priority 1: Must Do\n(Fix Bugs & Run Benchmarks)"] --> P2["Priority 2: Should Do\n(Embed Edge ML & Adaptive Gossip)"]
    P2 --> P3["Priority 3: Nice to Have\n(Hardware Tests & Dynamic Partitioning)"]
```

### Priority 1: Must Do (Critical Requirements)
1. **Fix Gossip Sample Inflation Bug:** Modify `sync()` in `east.py`, `west.py`, `central.py` to use windowed timestamp vectors instead of accumulating raw sample counts.
2. **Fix Food Prep Case-Sensitivity Bug:** Add `.lower()` string normalization in `utils.get_prep_time`.
3. **Add Cross-Region Exception Handling:** Wrap peer REST calls in `custom_eta()` with `try-except` blocks and HTTP timeouts.
4. **Build Benchmark Execution Suite:** Implement `experiments/run_benchmarks.py` to execute Experiments A through E and generate empirical latency CDFs, throughput curves, and gossip convergence data.
5. **Align Paper Text with Code:** Update manuscript text to retract false ML and cloud proxy claims, framing current prototype as an architectural edge platform.

---

### Priority 2: Should Do (Strong Enhancements)
1. **Embed Edge ML Model:** Train a lightweight ONNX LightGBM model on open urban delivery data and host inference inside `/custom_eta` endpoints.
2. **Implement Workload-Aware Gossip:** Add adaptive tick sleep calculation $\Delta t \in [1\text{s}, 30\text{s}]$ based on request velocity.
3. **Environment-Based Config:** Replace hardcoded `localhost` URLs with `os.getenv` environment variables.

---

### Priority 3: Nice to Have (Optional Polish)
1. **Physical Edge Node Deployment:** Benchmark microservices on 3 physical Raspberry Pi 4 / NVIDIA Jetson boards.
2. **Dynamic Voronoi Spatial Partitioning:** Implement real-time boundary adjustment driven by request density.
