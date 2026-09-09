# EdgeSync Scalability Experiment — Raw Data Audit

**Audit Execution Timestamp:** `2026-08-25 23:51:18`  
**Total Raw CSV Files Verified:** `63 / 63`  
**Total Measured Observations:** `6300` (100 requests × 63 runs)  
**Total Warm-Up Requests:** `1,260` requests (20 per run, strictly isolated)  
**Audit Status:** `PASSED`

---

## 1. Compliance Checklist

- [x] Every expected raw CSV exists (63/63 files)
- [x] Exactly 3 trials per experimental condition
- [x] Exactly 100 measured requests per run
- [x] Warm-up excluded from all statistics calculations
- [x] Request IDs unique within every raw dataset
- [x] Workload hashes identical across architectures for corresponding trials
- [x] No duplicate observations
- [x] No malformed rows or missing columns
- [x] No unexpected NaNs in measurement fields
- [x] Success and failure counts dynamically verified from HTTP status codes
- [x] Latency statistics (P50, P90, P95, P99, mean, stddev) reproducible directly from raw CSVs
- [x] Throughput reproducible from measured benchmark intervals
- [x] No hard-coded statistics or significance values
- [x] Figures generated dynamically from active raw datasets
- [x] Statistics tables generated dynamically from active raw datasets

## 2. Granular Trial Inventory Table

| Architecture | Concurrency | Trial | N | Success | Failed | Avail (%) | Throughput (req/s) | P50 (ms) | P95 (ms) | P99 (ms) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| centralized | 1 | trial1 | 100 | 100 | 0 | 100.0% | 413.22 | 2.230 | 3.211 | 3.605 |
| centralized | 1 | trial2 | 100 | 100 | 0 | 100.0% | 446.43 | 2.129 | 2.543 | 3.261 |
| centralized | 1 | trial3 | 100 | 100 | 0 | 100.0% | 440.53 | 2.140 | 2.694 | 2.884 |
| centralized | 2 | trial1 | 100 | 100 | 0 | 100.0% | 617.28 | 3.102 | 4.715 | 6.302 |
| centralized | 2 | trial2 | 100 | 100 | 0 | 100.0% | 546.45 | 2.831 | 7.344 | 8.789 |
| centralized | 2 | trial3 | 100 | 100 | 0 | 100.0% | 641.03 | 2.803 | 4.231 | 5.119 |
| centralized | 4 | trial1 | 100 | 100 | 0 | 100.0% | 613.50 | 6.382 | 9.541 | 10.650 |
| centralized | 4 | trial2 | 100 | 100 | 0 | 100.0% | 602.41 | 6.657 | 9.610 | 10.510 |
| centralized | 4 | trial3 | 100 | 100 | 0 | 100.0% | 561.80 | 7.008 | 9.684 | 30.192 |
| centralized | 8 | trial1 | 100 | 100 | 0 | 100.0% | 578.03 | 13.107 | 21.894 | 24.014 |
| centralized | 8 | trial2 | 100 | 100 | 0 | 100.0% | 602.41 | 13.306 | 18.487 | 20.660 |
| centralized | 8 | trial3 | 100 | 100 | 0 | 100.0% | 609.76 | 12.525 | 18.124 | 22.831 |
| centralized | 16 | trial1 | 100 | 100 | 0 | 100.0% | 653.59 | 20.626 | 31.724 | 33.967 |
| centralized | 16 | trial2 | 100 | 100 | 0 | 100.0% | 680.27 | 21.176 | 32.013 | 34.493 |
| centralized | 16 | trial3 | 100 | 100 | 0 | 100.0% | 675.68 | 21.929 | 32.825 | 33.287 |
| centralized | 32 | trial1 | 100 | 100 | 0 | 100.0% | 606.06 | 31.182 | 52.230 | 65.764 |
| centralized | 32 | trial2 | 100 | 100 | 0 | 100.0% | 606.06 | 32.448 | 51.662 | 57.889 |
| centralized | 32 | trial3 | 100 | 100 | 0 | 100.0% | 588.24 | 33.836 | 61.602 | 72.941 |
| centralized | 64 | trial1 | 100 | 100 | 0 | 100.0% | 546.45 | 35.244 | 66.192 | 75.646 |
| centralized | 64 | trial2 | 100 | 100 | 0 | 100.0% | 574.71 | 36.588 | 59.839 | 64.951 |
| centralized | 64 | trial3 | 100 | 100 | 0 | 100.0% | 561.80 | 37.645 | 57.338 | 62.719 |
| edgesync_local | 1 | trial1 | 100 | 100 | 0 | 100.0% | 378.79 | 2.484 | 3.387 | 4.074 |
| edgesync_local | 1 | trial2 | 100 | 100 | 0 | 100.0% | 409.84 | 2.329 | 2.917 | 3.047 |
| edgesync_local | 1 | trial3 | 100 | 100 | 0 | 100.0% | 390.62 | 2.369 | 3.479 | 3.900 |
| edgesync_local | 2 | trial1 | 100 | 100 | 0 | 100.0% | 657.89 | 2.757 | 4.741 | 6.542 |
| edgesync_local | 2 | trial2 | 100 | 100 | 0 | 100.0% | 467.29 | 3.980 | 7.925 | 12.054 |
| edgesync_local | 2 | trial3 | 100 | 100 | 0 | 100.0% | 549.45 | 3.351 | 5.563 | 25.297 |
| edgesync_local | 4 | trial1 | 100 | 100 | 0 | 100.0% | 529.10 | 7.303 | 11.624 | 18.363 |
| edgesync_local | 4 | trial2 | 100 | 100 | 0 | 100.0% | 641.03 | 6.196 | 8.809 | 9.038 |
| edgesync_local | 4 | trial3 | 100 | 100 | 0 | 100.0% | 537.63 | 7.221 | 10.901 | 12.491 |
| edgesync_local | 8 | trial1 | 100 | 100 | 0 | 100.0% | 657.89 | 12.005 | 18.100 | 20.144 |
| edgesync_local | 8 | trial2 | 100 | 100 | 0 | 100.0% | 657.89 | 11.684 | 17.959 | 20.007 |
| edgesync_local | 8 | trial3 | 100 | 100 | 0 | 100.0% | 632.91 | 12.959 | 18.370 | 21.260 |
| edgesync_local | 16 | trial1 | 100 | 100 | 0 | 100.0% | 641.03 | 23.438 | 35.090 | 39.895 |
| edgesync_local | 16 | trial2 | 100 | 100 | 0 | 100.0% | 602.41 | 23.104 | 34.966 | 43.763 |
| edgesync_local | 16 | trial3 | 100 | 100 | 0 | 100.0% | 625.00 | 21.257 | 33.575 | 39.242 |
| edgesync_local | 32 | trial1 | 100 | 100 | 0 | 100.0% | 558.66 | 33.958 | 60.630 | 78.425 |
| edgesync_local | 32 | trial2 | 100 | 100 | 0 | 100.0% | 523.56 | 41.093 | 66.234 | 80.367 |
| edgesync_local | 32 | trial3 | 100 | 100 | 0 | 100.0% | 561.80 | 34.324 | 57.122 | 66.818 |
| edgesync_local | 64 | trial1 | 100 | 100 | 0 | 100.0% | 502.51 | 37.949 | 60.645 | 75.273 |
| edgesync_local | 64 | trial2 | 100 | 100 | 0 | 100.0% | 529.10 | 34.850 | 63.000 | 77.975 |
| edgesync_local | 64 | trial3 | 100 | 100 | 0 | 100.0% | 512.82 | 37.095 | 61.878 | 79.788 |
| edgesync_remote | 1 | trial1 | 100 | 100 | 0 | 100.0% | 165.29 | 5.974 | 7.202 | 7.501 |
| edgesync_remote | 1 | trial2 | 100 | 100 | 0 | 100.0% | 160.00 | 6.033 | 8.782 | 10.031 |
| edgesync_remote | 1 | trial3 | 100 | 100 | 0 | 100.0% | 177.62 | 5.513 | 6.927 | 7.291 |
| edgesync_remote | 2 | trial1 | 100 | 100 | 0 | 100.0% | 223.21 | 8.975 | 10.358 | 11.735 |
| edgesync_remote | 2 | trial2 | 100 | 100 | 0 | 100.0% | 224.72 | 9.149 | 11.168 | 11.694 |
| edgesync_remote | 2 | trial3 | 100 | 100 | 0 | 100.0% | 225.73 | 8.805 | 11.264 | 11.762 |
| edgesync_remote | 4 | trial1 | 100 | 100 | 0 | 100.0% | 304.88 | 13.489 | 17.365 | 18.675 |
| edgesync_remote | 4 | trial2 | 100 | 100 | 0 | 100.0% | 289.86 | 14.392 | 17.698 | 18.016 |
| edgesync_remote | 4 | trial3 | 100 | 100 | 0 | 100.0% | 279.33 | 15.412 | 18.392 | 20.220 |
| edgesync_remote | 8 | trial1 | 100 | 100 | 0 | 100.0% | 331.13 | 25.051 | 33.871 | 36.334 |
| edgesync_remote | 8 | trial2 | 100 | 100 | 0 | 100.0% | 307.69 | 26.940 | 34.273 | 37.277 |
| edgesync_remote | 8 | trial3 | 100 | 100 | 0 | 100.0% | 326.80 | 25.417 | 33.920 | 36.286 |
| edgesync_remote | 16 | trial1 | 100 | 100 | 0 | 100.0% | 323.62 | 50.654 | 58.780 | 76.213 |
| edgesync_remote | 16 | trial2 | 100 | 100 | 0 | 100.0% | 343.64 | 46.069 | 57.583 | 61.976 |
| edgesync_remote | 16 | trial3 | 100 | 100 | 0 | 100.0% | 355.87 | 46.369 | 54.539 | 66.841 |
| edgesync_remote | 32 | trial1 | 100 | 100 | 0 | 100.0% | 314.47 | 85.948 | 167.737 | 210.052 |
| edgesync_remote | 32 | trial2 | 100 | 100 | 0 | 100.0% | 321.54 | 86.874 | 182.807 | 242.461 |
| edgesync_remote | 32 | trial3 | 100 | 100 | 0 | 100.0% | 332.23 | 83.456 | 167.510 | 217.494 |
| edgesync_remote | 64 | trial1 | 100 | 100 | 0 | 100.0% | 294.12 | 94.573 | 193.959 | 195.780 |
| edgesync_remote | 64 | trial2 | 100 | 100 | 0 | 100.0% | 303.95 | 89.131 | 172.979 | 178.688 |
| edgesync_remote | 64 | trial3 | 100 | 100 | 0 | 100.0% | 265.96 | 113.932 | 218.354 | 225.325 |

