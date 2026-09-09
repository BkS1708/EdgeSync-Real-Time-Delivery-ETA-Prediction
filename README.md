# 🚚 EdgeSync: Real-Time Delivery ETA Prediction

> **Locality-Aware Decentralized Edge Microservices for Low-Latency Spatial Estimation and Fault-Resilient Distributed Routing**

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-FastAPI%20%7C%20Streamlit-green.svg)](https://fastapi.tiangolo.com/)
[![Research Target](https://img.shields.io/badge/research-IEEE%20PerCom%202027-orange.svg)](results/PERCOM_PAPER_BLUEPRINT.md)
[![Availability](https://img.shields.io/badge/availability-100.0%25%20(Fault--Tolerant)-brightgreen.svg)](results/fault_tolerance/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

---

## 📌 Executive Summary

**EdgeSync** is an edge-native, decentralized simulation and estimation architecture designed for hyper-local delivery platforms (e.g., Swiggy, Zomato, Uber Eats). Standard centralized cloud architectures route spatial ETA prediction requests across wide-area networks (WAN), incurring high network latency ($30\text{--}80\text{ ms}$), bandwidth bottlenecks, and single-point-of-failure risks during network partitions or cloud outages.

EdgeSync tackles this challenge by deploying lightweight, autonomous edge microservices directly across geographic partitions (modeled across Mumbai's **EAST**, **WEST**, and **CENTRAL** regions). EdgeSync combines:
1. **Spatial Geofencing & Locality Routing**: Processing intra-region orders entirely at the local edge ($L_{\text{sys}} \approx 1.61\text{ ms}$).
2. **Decentralized Gossip State Synchronization**: A Conflict-free Replicated Data Type (CRDT) observation store synchronized across edge nodes using vector clocks without requiring a centralized coordinator.
3. **Autonomous Local Fallback**: Circuit-breaking and graceful local degradation ensuring **100.0% request availability** during node crashes or WAN disconnects.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Clients["Ingress & Presentation Layer"]
        User["Rider / Customer App"]
        UI["Streamlit Interactive UI\n(:8501)"]
        User -->|Spatial Queries & Traffic Setting| UI
    end

    subgraph EdgeNodes["EdgeSync Microservice Mesh (FastAPI)"]
        subgraph EastNode["EAST Region Edge (:8000)"]
            E_API["REST / ASGI Dispatcher"]
            E_Geo["Spatial Geofence"]
            E_State["Vector Clock & State Store"]
            E_Fall["Autonomous Fallback Engine"]
        end

        subgraph WestNode["WEST Region Edge (:9000)"]
            W_API["REST / ASGI Dispatcher"]
            W_Geo["Spatial Geofence"]
            W_State["Vector Clock & State Store"]
            W_Fall["Autonomous Fallback Engine"]
        end

        subgraph CentralNode["CENTRAL Region Edge (:10000)"]
            C_API["REST / ASGI Dispatcher"]
            C_Geo["Spatial Geofence"]
            C_State["Vector Clock & State Store"]
            C_Fall["Autonomous Fallback Engine"]
        end
    end

    UI -->|HTTP /predict| E_API
    UI -->|HTTP /predict| W_API
    UI -->|HTTP /predict| C_API

    E_API <-->|Gossip Synchronization\n(Vector Clocks / Observations)| W_API
    W_API <-->|Gossip Synchronization\n(Vector Clocks / Observations)| C_API
    C_API <-->|Gossip Synchronization\n(Vector Clocks / Observations)| E_API
```

### Request Lifecycle & Routing Mechanics

1. **Ingress & Geofence Check**: An ETA request $(o, d)$ is received by the ingress edge node. If the destination $d$ falls within the node's local boundary, the ETA calculation is performed immediately in-memory with sub-millisecond overhead.
2. **Cross-Region Delegation**: If $d$ belongs to a neighboring edge region, the request is delegated asynchronously over HTTP/1.1 connection pools.
3. **Autonomous Fallback Execution**: If the destination edge node is unresponsive, timed out, or severed by a partition, the local node automatically activates fallback estimation logic, logging a degraded status while returning a valid ETA estimate with **zero HTTP 500 errors**.
4. **Decentralized Synchronization**: Nodes periodically exchange weighted moving averages and observation counts through gossip rounds to reconcile city-wide traffic state convergence.

---

## 🔬 Key Scientific & Empirical Highlights (IEEE PerCom Evaluation)

EdgeSync has undergone rigorous evaluation across $>19,200$ controlled requests in a multi-trial testbed. Key empirical takeaways include:

| Metric Dimension | Canonical Empirical Result | Statistical Rigor |
| :--- | :--- | :--- |
| **Local Software Overhead** | **$1.609\text{ ms}$ (P50)**, $2.14\text{ ms}$ (P90) | Monolithic baseline delta is only $+0.25\text{ ms}$ ($N=1,000$) |
| **Peak Concurrency Throughput** | **$650.06\text{ RPS}$** at Concurrency $C=8$ | Sustains $>520\text{ RPS}$ up to $C=64$ ($N=6,300$) |
| **High Availability Under Crash** | **$100.0\%$ availability** (0 failures) | Autonomous fallback verified across 9 failure scenarios ($N=600$) |
| **Locality Delay Shielding** | **Spearman $\rho = -1.0, p < 0.001$** | Median latency shielded ($1.55\text{ ms} \to 1.71\text{ ms}$) under L90 ($N=9,000$) |
| **Gossip Convergence** | Divergence drops to $0.0$ in **$1.2\text{--}2.6\text{ s}$** | Fully connected topology converges in $<1.2\text{ s}$ |

> See [`results/PERCOM_PAPER_BLUEPRINT.md`](results/PERCOM_PAPER_BLUEPRINT.md) and [`results/PERCOM_CLAIM_EVIDENCE_MATRIX.md`](results/PERCOM_CLAIM_EVIDENCE_MATRIX.md) for full statistical audits and claim verification matrices.

---

## 📂 Repository Organization

```bash
EdgeSync-ETA/
├── central.py                  # CENTRAL region FastAPI microservice (:10000)
├── east.py                     # EAST region FastAPI microservice (:8000)
├── west.py                     # WEST region FastAPI microservice (:9000)
├── utils.py                    # Core domain logic (Haversine, traffic factors, ETA models)
├── config.py                   # Node topologies, boundaries, and endpoint configuration
├── ui.py                       # Streamlit visual map dashboard & gossip monitor
├── requirements.txt            # Python environment dependencies
│
├── experiments/                # Rigorous experimental benchmarking harness
│   ├── run_all.py              # Master benchmark orchestration script
│   ├── validate_results.py     # Reproducibility data validator
│   ├── runners/                # Specialized test runners (scalability, fault, network, locality)
│   ├── workloads/              # Synthetic request workload generators ($N=1000$ seed-controlled)
│   ├── baselines/              # Centralized cloud and monolithic baseline implementations
│   ├── analysis/               # Statistical processing, CDF analysis, and hypothesis testing
│   └── README.md               # Detailed guide to the benchmarking harness
│
├── research_docs/              # 29 in-depth architectural and research whitepapers
│   ├── DISTRIBUTED_STATE_MODEL.md      # Formal vector clock and CRDT mathematics
│   ├── FINAL_PERCOM_READINESS_REPORT.md# Readiness audit across 8 scientific dimensions
│   ├── 00_PROJECT_OVERVIEW.md to 20_FINAL_GAP_SUMMARY.md
│   └── README.md               # Master taxonomy and research document index
│
├── results/                    # Complete empirical data, charts, and PerCom paper artifacts
│   ├── PERCOM_PAPER_BLUEPRINT.md       # IEEE PerCom 2027 section-by-section drafting guide
│   ├── PERCOM_CLAIM_EVIDENCE_MATRIX.md # Evidence validation matrix for all paper claims
│   ├── PERCOM_FIGURE_PLAN.md           # Publication figure and chart inventory
│   ├── figures/                        # High-resolution PNG evaluation figures
│   ├── scalability/, fault_tolerance/, latency/, locality/, network_sensitivity/
│   └── README.md               # Experimental results catalog and data dictionary
│
├── tests/                      # Automated unit and property-based test suite
│   ├── test_units.py           # Unit tests (Haversine distance, speed formulas, boundaries)
│   ├── test_gossip_properties.py # Property tests (CRDT idempotence, commutativity, vector clocks)
│   └── README.md               # Test runner and verification guide
│
└── logs/                       # Gossip trace logs and runtime execution telemetry
    ├── gossip/                 # Real-time JSONL exchange logs (central, east, west)
    └── README.md               # Logging schemas and event replay instructions
```

---

## 🚀 Quickstart & Setup

### 1. Prerequisites & Environment Setup

Clone the repository and install required packages:
```bash
git clone https://github.com/BkS1708/EdgeSync-Real-Time-Delivery-ETA-Prediction.git
cd EdgeSync-Real-Time-Delivery-ETA-Prediction
pip install -r requirements.txt
```

### 2. Start the Edge Microservices

Launch each regional edge node in separate terminal windows:

```bash
# Terminal 1: EAST Region Edge Node
uvicorn east:app --host 127.0.0.1 --port 8000

# Terminal 2: WEST Region Edge Node
uvicorn west:app --host 127.0.0.1 --port 9000

# Terminal 3: CENTRAL Region Edge Node
uvicorn central:app --host 127.0.0.1 --port 10000
```

### 3. Launch the Interactive Dashboard

In a fourth terminal, launch the Streamlit frontend:
```bash
streamlit run ui.py
```
- Open your browser at `http://localhost:8501`.
- Select pickup and drop-off coordinates across Mumbai.
- Inspect real-time stage breakdowns (Preparation vs Pickup vs Delivery) and monitor decentralized gossip propagation live!

---

## 🧪 Automated Testing

EdgeSync includes unit and property-based tests verifying algorithmic correctness, vector clock monotonicity, and CRDT convergence:

```bash
python -m unittest discover tests
```

Output:
```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.002s

OK
```

---

## 📊 Reproducing Experimental Benchmarks

The entire empirical evaluation can be reproduced automatically:

```bash
# Run the complete testbed suite (Latency, Scalability, Fault Tolerance, Locality, Ablation)
python experiments/run_all.py

# Validate generated data integrity and schemas
python experiments/validate_results.py
```

Generated charts and summary tables will be written to `results/` in high-resolution format.

---

## 📑 Academic Publication & Citation

This codebase serves as the research prototype and experimental artifact for:

- **Title:** *EdgeSync: Locality-Aware Decentralized Edge Microservices for Low-Latency Spatial Estimation*
- **Target Venue:** IEEE International Conference on Pervasive Computing and Communications (PerCom)
- **Author:** Bhavya Sanghrajka ([@BkS1708](https://github.com/BkS1708))
- **Primary Blueprint:** [`results/PERCOM_PAPER_BLUEPRINT.md`](results/PERCOM_PAPER_BLUEPRINT.md)

If you find this work helpful in your research, please cite:
```bibtex
@inproceedings{sanghrajka2027edgesync,
  title={EdgeSync: Locality-Aware Decentralized Edge Microservices for Low-Latency Spatial Estimation},
  author={Sanghrajka, Bhavya},
  booktitle={IEEE International Conference on Pervasive Computing and Communications (PerCom)},
  year={2027}
}
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
