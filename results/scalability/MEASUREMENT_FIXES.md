# EdgeSync Scalability Experiment — Measurement & Statistics Integrity Fixes

**Audit & Fix Date/Time:** `2026-08-25 18:05:00`  
**Purpose:** Pre-experiment verification and formal specification of statistical calculation rules to guarantee 100% research integrity.

---

## 1. Measurement Integrity Principles Applied

### Rule 1: Dynamic Calculation of Availability
- **Formula:**
  $$\text{Availability (\%)} = \frac{N_{\text{successful\_measured}}}{N_{\text{total\_measured}}} \times 100$$
- **Verification:** Hard-coded constants (such as `100.0`) are strictly banned in all dictionary builders, CSV writers, and markdown report generators.

### Rule 2: Strict Isolation of Warm-Up Data
- **Mechanism:**
  - Every trial executes $20$ warm-up requests marked with `warmup=True` (or isolated in a pre-flight loop).
  - Only rows with `warmup=False` are loaded into statistical aggregation arrays and written to raw measurement tables.
  - Benchmark duration for throughput calculation starts **after** warm-up finishes.

### Rule 3: Explicit Representation of Failures & Timeouts
- **Failure Tracking:**
  - Any request returning HTTP status $\neq 200$ or raising a network exception is marked `success=False` with its actual HTTP status or `500` on exception.
  - Requests exceeding $10.0\text{ s}$ are flagged as timeouts and counted in `timeout_count`.
  - Failed requests are never omitted from total counts $N$ and never assigned synthetic latency values.

### Rule 4: Distinct Throughput Calculation
- **Definition:**
  $$\text{Throughput (req/sec)} = \frac{N_{\text{successful\_measured}}}{\Delta t_{\text{benchmark\_duration}}}$$
  Where $\Delta t_{\text{benchmark\_duration}} = t_{\text{last\_request\_completed}} - t_{\text{first\_request\_dispatched}}$ across all concurrent threads for the 100 measured requests.
- **Exclusions:** Setup time, node health-check time, and warm-up time are strictly excluded from $\Delta t_{\text{benchmark\_duration}}$.

### Rule 5: Unique Request Identification & Workload Hashing
- **Request IDs:** Format `req_{concurrency}_{trial}_{index:04d}` guaranteeing global uniqueness within every raw CSV.
- **Workload Hash:** Computed as `SHA-256` of canonical JSON request arrays, ensuring exact identical payload delivery across Centralized, EdgeSync Local, and EdgeSync Cross-Region.

---

## 2. Inventory of Specific Code Safeguards

| Component | Potential Vulnerability | Implemented Safeguard |
| :--- | :--- | :--- |
| **Availability Aggregator** | Hard-coded default | `availability_pct = round((succ / max(1, total)) * 100.0, 2)` |
| **Percentile Engine** | Stale summary reuse | `calculate_stats()` computed on-the-fly from active raw CSV column arrays |
| **Thread Sessions** | Socket connection contention | Thread-local `requests.Session()` pools preventing TCP cross-thread locking |
| **Statistical Tests** | Hard-coded significance | Exact Wilcoxon signed-rank statistics computed with `scipy.stats.wilcoxon` + Holm-Bonferroni adjustment |
| **Report Generation** | Narrative drift | 100% of tables and numerical narrative tokens dynamically formatted from calculated dataframes |
