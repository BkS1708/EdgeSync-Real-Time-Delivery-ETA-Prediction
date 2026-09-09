# 🔬 EdgeSync Experimental Benchmarking Testbed

This directory contains the complete automated experimental evaluation harness for the **EdgeSync** research project. The harness benchmarks system overhead, spatial locality, gossip convergence, concurrency scalability, network delay insulation, and fault tolerance across thousands of controlled requests.

---

## 🏗️ Architecture of the Testbed

```text
experiments/
├── run_all.py                  # Master runner to execute the full evaluation suite
├── validate_results.py         # Integrity checker for generated CSV/JSON artifacts
├── runners/                    # Specialized per-dimension benchmark runners
│   ├── run_latency_experiment.py             # System vs domain latency profiling
│   ├── run_controlled_latency_experiment.py  # Precision software overhead calibration
│   ├── run_scalability_experiment.py         # Concurrency sweep (C = 1 to 64)
│   ├── run_full_scalability_experiment.py    # Multi-trial throughput vs load sweep
│   ├── run_fault_tolerance_experiment.py     # Peer failure & circuit-breaker injection
│   ├── complete_fault_tolerance_suite.py     # 9-scenario failure matrix evaluation
│   ├── run_locality_experiment.py            # Spatial locality sweep (L10 to L90)
│   ├── run_network_sensitivity_experiment.py # WAN delay & jitter sensitivity (0-100ms)
│   ├── run_gossip_experiment.py              # Convergence time across network topologies
│   ├── run_partition_experiment.py           # Network partition & healing evaluation
│   ├── run_ablation_experiment.py            # Component ablation (Gossip vs Static vs Central)
│   └── run_smoke_test.py                     # Fast end-to-end verification pipeline
├── workloads/                  # Workload generation and canonical datasets
│   ├── generator.py            # Deterministic, seed-controlled spatial coordinate generator
│   └── benchmark_workload.json # Canonical benchmark workload (N=1,000, seed=42)
├── baselines/                  # Comparative baseline systems
│   ├── centralized_server.py   # Cloud-centric monolithic architecture
│   └── hybrid_server.py        # Semi-distributed edge-cloud tiering baseline
├── network/                    # Synthetic delay and network condition emulators
│   └── network_emulator.py     # Configurable latency, jitter, and packet loss injection
├── metrics/                    # Telemetry and statistics collectors
│   └── collector.py            # High-resolution timing (P50, P90, P99) and resource monitoring
├── plots/                      # Publication chart generators
│   └── plotter.py              # Generates publication-ready CDFs, timelines, and bar charts
└── analysis/                   # Statistical validation and auditing
    ├── statistics.py           # Welch's t-tests, ANOVA, Spearman rank correlation, confidence intervals
    ├── audit_scalability_full.py
    └── audit_raw_fault_tolerance.py
```

---

## 🚀 Running Experiments

### Prerequisites

Ensure the edge microservices are either running locally or can be automatically spun up by the test harness:
```bash
# Verify microservice endpoints
curl http://127.0.0.1:8000/docs   # East
curl http://127.0.0.1:9000/docs   # West
curl http://127.0.0.1:10000/docs  # Central
```

### 1. Execute All Experiments (Full Paper Suite)

To run the end-to-end evaluation suite and regenerate all figures and statistics:
```bash
python experiments/run_all.py
```
This script orchestrates the benchmarks sequentially, logs raw CSV telemetry, computes statistical summaries, and writes publication figures into `results/`.

### 2. Run Individual Experiment Runners

Each dimension can be independently executed and calibrated:

#### A. Spatial Locality Benchmark
Sweeps locality ratios from 10% to 90% across 3,000 requests to measure cross-region routing penalties:
```bash
python experiments/runners/run_locality_experiment.py
```

#### B. Network Sensitivity & Shielding
Evaluates cluster resilience against synthetic WAN latency injection (0 ms to 100 ms) with 9,000 requests:
```bash
python experiments/runners/run_network_sensitivity_experiment.py
```

#### C. Concurrency & Scalability Sweep
Evaluates throughput (RPS) and latency percentiles under concurrent client workers ($C \in \{1, 2, 4, 8, 16, 32, 64\}$):
```bash
python experiments/runners/run_full_scalability_experiment.py
```

#### D. Fault Tolerance & Autonomous Fallback
Simulates peer process termination, socket timeouts, and network partitions across 9 failure scenarios:
```bash
python experiments/runners/complete_fault_tolerance_suite.py
```

#### E. Gossip Protocol Convergence
Measures the number of exchange rounds and wall-clock seconds required for peer state convergence:
```bash
python experiments/runners/run_gossip_experiment.py
```

---

## 🔍 Validation & Reproducibility

To audit generated experimental data files for completeness and schema compliance:
```bash
python experiments/validate_results.py
```

All experimental outputs are saved in structured formats:
- Raw request logs: `results/<dimension>/raw/`
- Statistical aggregates: `results/<dimension>/statistics/`
- High-resolution figures: `results/<dimension>/figures/` or `results/figures/`
