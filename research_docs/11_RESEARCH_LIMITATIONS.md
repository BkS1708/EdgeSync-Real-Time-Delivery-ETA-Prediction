# EdgeSync Research Dossier: Research Limitations Analysis

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `11_RESEARCH_LIMITATIONS.md`

---

## 1. Executive Summary

This document categorizes all technical, architectural, algorithmic, and experimental limitations discovered in the actual EdgeSync source code (`EdgeSync-ETA-main`). Each limitation is evaluated for its impact and marked with a PerCom Readiness Priority (**MUST FIX**, **SHOULD FIX**, or **DOCUMENT AS FUTURE WORK**).

---

## 2. Categorized Technical Limitations

### Category A: Architectural & Infrastructure Limitations

1. **Hardcoded Microservice Networking:**
   - *Why It Exists:* Inter-node URLs (`http://localhost:8000`, `9000`, `10000`) are explicitly defined in dictionaries inside Python source files ([`east.py:L47-L49`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L47-L49)).
   - *Impact:* Cannot deploy across real distributed edge servers, Docker containers, or Kubernetes clusters without editing Python code.
   - *Fix:* Replace hardcoded string dictionaries with environment variables (`os.getenv("WEST_NODE_URL")`) or a lightweight Consul/Etcd service registry.
   - *PerCom Priority:* **MUST FIX** (Essential for real distributed edge deployment).

2. **Static Spatial Boundaries:**
   - *Why It Exists:* Bounding box thresholds (`lat < 19.05`, `lon < 72.85`) are hardcoded in [`config.py:L2, L4`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/config.py#L2).
   - *Impact:* System cannot scale dynamically to $N$ regions or adjust boundaries based on fluctuating regional order volumes.
   - *Fix:* Implement dynamic voronoi partitioning or quadtree spatial indexing.
   - *PerCom Priority:* **SHOULD FIX** (Strong research improvement).

---

### Category B: Distributed Systems & Synchronization Limitations

1. **Sample Inflation & Lack of Gossip Idempotency:**
   - *Why It Exists:* `sync()` adds incoming sample counts to local samples unconditionally on every 5-second tick ([`east.py:L120-L128`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L120-L128)).
   - *Impact:* Over time, sample counts exponentially blow up and destroy historical accuracy, violating the paper's theoretical claims.
   - *Fix:* Implement timestamped epoch windows or CRDTs (Conflict-free Replicated Data Types) for sample aggregation.
   - *PerCom Priority:* **MUST FIX** (Resolves major scientific contradiction).

2. **Unhandled Cross-Region Cascading Failures:**
   - *Why It Exists:* Cross-region `requests.post()` calls in `custom_eta()` lack `try-except` blocks and timeout configurations ([`east.py:L52-L56`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L52-L56)).
   - *Impact:* A single node crash causes unhandled HTTP exceptions on peer nodes during cross-region requests.
   - *Fix:* Wrap inter-service REST calls in `try-except` blocks with a fallback local distance computation and circuit breaker pattern.
   - *PerCom Priority:* **MUST FIX** (Critical for proving fault tolerance).

---

### Category C: Algorithmic & ETA Model Limitations

1. **Absence of Machine Learning Models:**
   - *Why It Exists:* ETA is computed purely via Haversine distance divided by static speed constants ($15, 25, 35\text{ km/h}$) ([`utils.py:L21-L28`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L21-L28)).
   - *Impact:* Model fails to capture road network geometry, turn delays, traffic lights, elevation, or complex spatio-temporal patterns.
   - *Fix:* Train a lightweight LightGBM or XGBoost regression model on open delivery datasets (e.g. Uber Movement or OSM) and embed model inference in the FastAPI endpoints.
   - *PerCom Priority:* **SHOULD FIX** (Substantially elevates scientific contribution).

2. **Food Prep Category Case-Sensitivity Bug:**
   - *Why It Exists:* UI sends capitalized strings (`"Pizza"`), dictionary expects lowercase (`"pizza"`) ([`utils.py:L54-L61`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L54-L61)).
   - *Impact:* UI requests always fall back to default prep range `(5, 10)`.
   - *Fix:* Normalize input string: `food.lower()`.
   - *PerCom Priority:* **MUST FIX** (Trivial 1-line code fix).

---

### Category D: Evaluation & Dataset Limitations

1. **Zero Quantitative Measurement Scripts:**
   - *Why It Exists:* The repository contains no benchmark scripts, load generators, or evaluation logs.
   - *Impact:* All paper performance claims (latency reduction, scalability, fault tolerance) are currently unbacked by repository evidence.
   - *Fix:* Build an automated benchmarking harness (`experiments/run_benchmarks.py`).
   - *PerCom Priority:* **MUST FIX** (Mandatory for PerCom acceptance).
