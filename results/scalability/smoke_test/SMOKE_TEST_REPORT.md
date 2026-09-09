# EdgeSync Scalability Experiment — Smoke Test Report

**Execution Date/Time:** `2026-08-25 23:46:08`  
**Smoke Test Status:** `PASSED`  
**Total Runs:** `9` (3 Architectures × 3 Concurrency Levels: 1, 4, 16)  
**Total Measured Requests:** `180` requests (20 per condition)  

---

## 1. Validation Summary

- [x] **All 9 smoke test combinations executed:** `PASS`
- [x] **All 9 raw CSV files exist:** `PASS`
- [x] **No failed requests across smoke test:** `PASS`
- [x] **100% availability achieved:** `PASS`
- [x] **Throughput values positive and non-zero:** `PASS`
- [x] **Plausible P50 latency (< 5ms at c=1, < 200ms at c=16):** `PASS`

## 2. Smoke Test Results Table

| Architecture | Concurrency | N | Success | Avail (%) | Throughput (req/s) | P50 (ms) | P95 (ms) | P99 (ms) | Mean (ms) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| centralized | 1 | 20 | 20 | 100.0% | 325.57 | 2.750 | 3.836 | 5.337 | 2.886 |
| centralized | 4 | 20 | 20 | 100.0% | 509.91 | 6.449 | 10.546 | 10.996 | 6.982 |
| centralized | 16 | 20 | 20 | 100.0% | 452.34 | 16.854 | 24.915 | 25.208 | 16.068 |
| edgesync_local | 1 | 20 | 20 | 100.0% | 254.72 | 2.478 | 3.629 | 25.492 | 3.778 |
| edgesync_local | 4 | 20 | 20 | 100.0% | 475.26 | 6.733 | 10.169 | 10.490 | 7.129 |
| edgesync_local | 16 | 20 | 20 | 100.0% | 417.59 | 15.972 | 28.340 | 29.214 | 17.244 |
| edgesync_remote | 1 | 20 | 20 | 100.0% | 191.61 | 4.637 | 6.274 | 6.436 | 5.069 |
| edgesync_remote | 4 | 20 | 20 | 100.0% | 231.98 | 16.179 | 20.700 | 22.068 | 15.823 |
| edgesync_remote | 16 | 20 | 20 | 100.0% | 249.56 | 43.435 | 56.661 | 56.883 | 42.012 |

## 3. Pre-Flight Conclusion

All pre-flight validation checks passed. The experimental infrastructure, thread pooling, socket sessions, decomposed latency tracking, and throughput measurement are functioning reliably and are approved for the full 6,300-request scalability experiment.
