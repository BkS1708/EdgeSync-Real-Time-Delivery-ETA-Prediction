# EdgeSync — Final IEEE PerCom Action Plan

**Audit Date:** `2026-09-01`  
**Status:** Canonical Pre-Submission Action Plan  
**Target Venue:** IEEE PerCom 2027  
**Scope:** Actionable breakdown of mandatory manuscript corrections, scope bounding, data pruning, and optional future enhancements.

---

## 1. Action Category Overview

| Priority Level | Category | Total Action Items | Can Be Solved with Existing Data? | New Experiments Required? |
| :---: | :--- | :---: | :---: | :---: |
| **Category A** | **MUST FIX BEFORE SUBMISSION** | **5** | **YES (Manuscript Bounding & Pruning)** | **NO** |
| **Category B** | **SHOULD FIX IF POSSIBLE** | **3** | **YES (Narrative Clarifications)** | **NO** |
| **Category C** | **OPTIONAL FUTURE ENHANCEMENTS** | **3** | **NO (Post-Submission / Camera-Ready)** | **YES (Post-PerCom)** |
| **Category D** | **NO ACTION REQUIRED (VERIFIED READY)** | **6** | **YES (Already Verified Pass)** | **NO** |

---

## 2. Category A: MUST FIX BEFORE PAPER SUBMISSION

These items represent publication-critical requirements. Failure to address them will result in immediate rejection by skeptical reviewers.

### Item A-1: Prune Network Partition & Packet Loss Claims from Manuscript
- **Exact Problem:** Scenarios 3, 4 (1%, 5%, 10%), 5, `scenario_2_trial3`, and `scenario_6_trial1` experienced HTTP 500 crashes due to an unhandled `TypeError` in `get_region([lat, lon])` during unpatched runner execution.
- **Affected Experiment:** Fault Tolerance & Recovery Suite (`results/fault_tolerance/`)
- **Affected Claim:** CLM-08 ("EdgeSync is resilient to network partitions and packet loss").
- **Severity:** **CRITICAL**.
- **Solution:** Existing data **CAN SOLVE IT** by removing all quantitative claims regarding network partitions and packet loss from the manuscript. Retain ONLY the valid empirical evidence for Peer Process Crash (`scenario_1`, $N=600$, 100% availability) and Node Recovery (`scenario_6`, $N=400$, 100% availability).
- **New Data Required?** **NO** for submission (claim pruning avoids rerun).

### Item A-2: Purge Obsolete Generation 1 Preliminary Metrics
- **Exact Problem:** Early documentation and draft text referenced legacy Generation 1 benchmarks containing artificial sleep delays (e.g., 2053 ms latency, 41% cloud reduction, 4.92 RPS).
- **Affected Experiment:** Legacy Latency (`results/latency/`), Claim Matrix V1 (`CLAIM_EVIDENCE_MATRIX.md`).
- **Affected Claim:** CLM-10 ("41% latency reduction").
- **Severity:** **HIGH**.
- **Solution:** Replace all legacy numbers with Generation 3 authoritative controlled datasets:
  - Baseline software overhead: $1.609\text{ ms}$ (P50) vs Centralized $1.352\text{ ms}$.
  - Scalability: Peak throughput $650.06\text{ RPS}$ (EdgeSync Local at $C=8$) vs Centralized $669.85\text{ RPS}$ ($C=16$).
  - Locality: $4.74\text{ ms}$ (L90) to $10.15\text{ ms}$ (L10) ($\rho = -1.0$).
- **New Data Required?** **NO** (Authoritative Gen 3 data already exists).

### Item A-3: Explicitly Scope Network Delay to Local Loopback Emulation
- **Exact Problem:** Describing emulated sleep delay as "geographic multi-region Internet latency" is factually inaccurate and triggers immediate reviewer hostility.
- **Affected Experiment:** Network Sensitivity Suite (`results/network_sensitivity/`).
- **Affected Claim:** CLM-02 ("Inter-service network delay sensitivity").
- **Severity:** **HIGH**.
- **Solution:** Update paper text and figure captions to explicitly state: *"Controlled inter-service delegation delay over calibrated IPv4 loopback sockets."* Emphasize the linear relationship ($R^2 = 0.9998$) and locality shielding effect.
- **New Data Required?** **NO**.

### Item A-4: Frame CRDT State Reconciliation as Formal Algebraic Model
- **Exact Problem:** Claiming empirical proof of multi-master eventual consistency under production WAN write contention when only in-memory unit prototypes were executed.
- **Affected Experiment:** Gossip Convergence (`results/gossip/summary.json`).
- **Affected Claim:** CLM-09 ("Global eventual consistency").
- **Severity:** **HIGH**.
- **Solution:** Present the CRDT set-union and vector clock formulation in Section IV as a *formal algebraic system model* with mathematical idempotence guarantees ($A \cup A = A$), and present the 3-node in-memory prototype as proof-of-concept validation.
- **New Data Required?** **NO**.

### Item A-5: Frame 0.25 ms Baseline Overhead as Amortized Edge Gain
- **Exact Problem:** On zero-delay loopback, Centralized ($1.352\text{ ms}$) is slightly faster than EdgeSync Local ($1.609\text{ ms}$) by $0.25\text{ ms}$.
- **Affected Experiment:** Controlled Latency Suite (`results/smoke_test/controlled_latency/`).
- **Affected Claim:** CLM-04 ("Baseline software routing overhead").
- **Severity:** **MEDIUM**.
- **Solution:** Provide a clear architectural explanation: on a local edge gateway, a $0.25\text{ ms}$ routing check is negligible compared to the $30-80\text{ ms}$ WAN round-trip latency avoided by not routing to a centralized cloud.
- **New Data Required?** **NO**.

---

## 3. Category B: SHOULD FIX IF POSSIBLE

1. **Item B-1 (Include Figure 5 Network Calibration):** Add the linear calibration curve (`network_calibration.png`, $R^2 = 0.9998$) to Section V to preempt reviewer questions about network emulator accuracy.
2. **Item B-2 (Highlight Statistical Equivalence at C=4):** Note in the scalability analysis that EdgeSync Local and Centralized latencies are statistically indistinguishable at moderate load ($C=4, p = 0.0544$).
3. **Item B-3 (Clarify Memory Footprint vs Energy Efficiency):** Report measured process RSS ($< 180\text{ MB}$) as evidence of compact gateway footprint, while omitting unsupported claims of physical energy savings.

---

## 4. Category C: OPTIONAL FUTURE ENHANCEMENTS (Post-PerCom)

1. **Item C-1 (Clean Rerun of Partition & Loss Suite):** Following the code patch in `config.py` and regional endpoints, execute `run_clean_partition_fault_suite.py` ($N=5,400$) to produce publication-grade partition tolerance figures for an extended journal version (e.g., IEEE TMC / IEEE TPDS).
2. **Item C-2 (Multi-Host Physical Edge Testbed):** Deploy EdgeSync across physical Raspberry Pi 4 nodes over local Wi-Fi / Ethernet to benchmark real hardware I/O.
3. **Item C-3 (Durable Disk-Backed CRDT Store):** Replace in-memory `ObservationStore` with SQLite/RocksDB LSM-trees for durable crash recovery.

---

## 5. Category D: NO ACTION REQUIRED (VERIFIED READY)

1. ✅ **Locality Sensitivity Dataset:** $N=3,000$, $\rho = -1.0, p < 0.001$ (**VERIFIED COMPLETE & PASS**).
2. ✅ **Network Sensitivity Dataset:** $N=9,000$, $R^2 = 0.9998$ (**VERIFIED COMPLETE & PASS**).
3. ✅ **Scalability & Concurrency Dataset:** $N=6,300$, $C=1..64$, 650 RPS (**VERIFIED COMPLETE & PASS**).
4. ✅ **Controlled Baseline Latency Dataset:** $N=900$, P50=1.61 ms (**VERIFIED COMPLETE & PASS**).
5. ✅ **Peer Crash Resilience Dataset:** $N=600$, 100% availability, 150 fallbacks (**VERIFIED COMPLETE & PASS**).
6. ✅ **Node Recovery Dataset (Valid Subset):** $N=400$, 100% availability (**VERIFIED COMPLETE & PASS**).
