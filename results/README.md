# 📊 EdgeSync Empirical Results & IEEE PerCom Publication Artifacts

This directory stores all empirical data, statistical evaluations, high-resolution figures, and manuscript preparation documents for the **EdgeSync** research project.

---

## 📑 Empirical Evaluation & Evidence Framework

The following master artifacts document the evaluation methodology and data audits:

| Document | Purpose & Key Contents |
| :--- | :--- |
| [`PERCOM_CLAIM_EVIDENCE_MATRIX.md`](PERCOM_CLAIM_EVIDENCE_MATRIX.md) | Strict mapping connecting every paper claim directly to underlying CSV files and p-values. |
| [`PERCOM_CLAIM_SAFETY_AUDIT.md`](PERCOM_CLAIM_SAFETY_AUDIT.md) | "Safe vs Forbidden" claim audit to protect the submission from reviewer rejection. |
| [`PERCOM_REVIEWER_ATTACK_ANALYSIS.md`](PERCOM_REVIEWER_ATTACK_ANALYSIS.md) | Comprehensive defense strategy detailing pre-empted reviewer objections and empirical rebuttals. |
| [`PERCOM_FIGURE_PLAN.md`](PERCOM_FIGURE_PLAN.md) | Final figure selection, sub-plots, and captions for the camera-ready manuscript. |
| [`PERCOM_TABLE_PLAN.md`](PERCOM_TABLE_PLAN.md) | LaTeX-ready table specifications (Experimental Parameters, Ablation, Fault Resilience). |
| [`PERCOM_LIMITATIONS.md`](PERCOM_LIMITATIONS.md) | Transparent disclosure of threats to validity, single-host emulation constraints, and edge constraints. |
| [`PERCOM_RAW_DATA_AUDIT.md`](PERCOM_RAW_DATA_AUDIT.md) | Verification and provenance audit of all generated CSV and JSON records. |
| [`FINAL_STATISTICAL_AUDIT.md`](FINAL_STATISTICAL_AUDIT.md) | Welch's t-tests ($p < 0.001$), ANOVA tables, and effect sizes ($d > 1.2$). |

---

## 📂 Empirical Benchmark Datasets by Dimension

```text
results/
├── latency/                    # Baseline & local software routing profiling
│   ├── latency_cdf.png         # Cumulative distribution function (CDF) of response times
│   ├── latency_summary.json    # Summary percentiles (P50: 1.609ms, P90: 2.14ms, P99: 4.88ms)
│   └── raw_results.csv         # Request-level telemetry across N=1,000 requests
│
├── locality/                   # Spatial locality sweep (L10 to L90)
│   ├── LOCALITY_EXPERIMENT_REPORT.md
│   ├── figures/                # Locality vs latency boxplots & regression curves
│   ├── raw/                    # Raw telemetry across N=3,000 requests
│   └── statistics/             # Spearman rank correlation (rho = -1.0, p < 0.001)
│
├── network_sensitivity/        # Injected WAN delay & jitter sensitivity
│   ├── NETWORK_SENSITIVITY_REPORT.md
│   ├── figures/                # Shielded median latency vs injected network delay
│   ├── raw/                    # Raw telemetry across N=9,000 requests
│   └── statistics/             # Linear regression data (R^2 = 0.9998)
│
├── scalability/                # Concurrency sweep (C=1 to 64)
│   ├── SCALABILITY_EXPERIMENT_REPORT.md
│   ├── throughput_vs_load.png  # Peak throughput curve (Peak: 650.06 RPS at C=8)
│   ├── resource_usage.png      # CPU and resident memory usage across concurrency levels
│   └── raw/, statistics/
│
├── fault_tolerance/            # Peer failure & circuit-breaker injection
│   ├── FAULT_TOLERANCE_REPORT.md
│   ├── fault_recovery_timeline.png # Recovery timeline and fallback activation
│   ├── summary.json            # 100.0% availability across 9 failure scenarios (N=600)
│   └── raw/
│
├── gossip/                     # Decentralized state reconciliation
│   ├── gossip_convergence.png  # Divergence decay curves across Ring vs Mesh topologies
│   └── summary.json            # Convergence time (1.2s to 2.6s)
│
├── ablation/                   # Architectural component ablation
│   ├── ablation_comparison.png # Comparison: Full EdgeSync vs Centralized vs Static ETA
│   └── ablation_summary.md     # Marginal contributions of gossip and local caching
│
├── smoke_test/                 # Integration test reports & sanity checks
│   └── SMOKE_TEST_REPORT.md
│
└── phase3/                     # Phase 3 consolidated research artifacts
    ├── experiment_metadata.json# Execution environment specs (Python 3.14, OS, hardware)
    └── figures/                # Publication-ready vectorized figures
```

---

## 📈 Canonical Metrics Summary

| Evaluation Suite | Sample Size ($N$) | Primary Metric | Outcome | Supporting Report |
| :--- | :---: | :--- | :--- | :--- |
| **System Latency** | $1,000$ | P50 software overhead | **$1.609\text{ ms}$** | [`latency/`](latency/) |
| **Concurrency Scalability** | $6,300$ | Peak Throughput | **$650.06\text{ RPS}$** ($C=8$) | [`scalability/`](scalability/) |
| **Fault Resilience** | $600$ | Request Availability | **$100.0\%$** (0 errors) | [`fault_tolerance/`](fault_tolerance/) |
| **Locality Sensitivity** | $3,000$ | Latency vs Locality | **$\rho = -1.0, p < 0.001$** | [`locality/`](locality/) |
| **Network Shielding** | $9,000$ | Median Delay Shift | **Shielded ($<0.16\text{ ms}$ shift)** | [`network_sensitivity/`](network_sensitivity/) |
| **Gossip Convergence** | rounds | State Reconciliation | **$<2.6\text{ s}$** (Ring), **$<1.2\text{ s}$** (Mesh)| [`gossip/`](gossip/) |
