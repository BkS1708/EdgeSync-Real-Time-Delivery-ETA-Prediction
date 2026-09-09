# EdgeSync — Controlled 100-Request Latency Validation Report

**Execution Date/Time:** `2026-08-25 09:15:13`  
**Total Execution Time:** `11.42 seconds`  
**Workload SHA-256 Hash:** `391bac7738c3a0b2b302febadd221936aea10b92f26bda6cc3dd048b4dd7ff85`  
**Total Measured Observations:** `900` (300 per trial across 3 trials)  

---

## 1. Executive Summary & Pooled Latency (N = 300 per Architecture)

| Architecture | N | Total Mean (ms) | Median | P50 | P90 | P95 | P99 | StdDev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Centralized | 300 | 1.406 | 1.352 | 1.352 | 1.683 | 1.855 | 2.251 | 0.236 |
| EdgeSync Local | 300 | 1.674 | 1.609 | 1.609 | 2.076 | 2.267 | 2.664 | 0.403 |
| EdgeSync Cross-Region | 300 | 2.68 | 2.929 | 2.929 | 3.638 | 3.936 | 4.526 | 0.883 |

## 2. Latency Component Breakdown

> **Nomenclature Note:** `Inter-Service Net` represents local/emulated inter-service communication overhead (peer REST HTTP over IPv4 loopback), NOT real geographic network latency.

| Architecture | System Mean (ms) | System P50 | System P95 | Inter-Service Net Mean (ms) | Inter-Service Net P50 | Inter-Service Net P95 | Domain Mean (ms) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Centralized | 0.082 | 0.085 | 0.174 | 0.0 | 0.0 | 0.0 | 0.082 |
| EdgeSync Local | 0.092 | 0.09 | 0.178 | 0.0 | 0.0 | 0.0 | 0.092 |
| EdgeSync Cross-Region | 0.101 | 0.093 | 0.196 | 1.011 | 1.444 | 2.005 | 0.101 |

## 3. Trial-to-Trial Consistency

| Trial | Architecture | Mean (ms) | P50 (ms) | P95 (ms) | P99 (ms) |
| --- | --- | --- | --- | --- | --- |
| trial_1 | Centralized | 1.418 | 1.368 | 1.875 | 2.272 |
| trial_1 | EdgeSync Local | 1.792 | 1.705 | 2.377 | 4.112 |
| trial_1 | EdgeSync Cross-Region | 2.627 | 2.942 | 3.725 | 4.102 |
| trial_2 | Centralized | 1.377 | 1.317 | 1.841 | 2.184 |
| trial_2 | EdgeSync Local | 1.495 | 1.455 | 1.788 | 1.945 |
| trial_2 | EdgeSync Cross-Region | 2.756 | 2.993 | 3.936 | 4.579 |
| trial_3 | Centralized | 1.424 | 1.367 | 1.853 | 2.241 |
| trial_3 | EdgeSync Local | 1.736 | 1.666 | 2.334 | 2.483 |
| trial_3 | EdgeSync Cross-Region | 2.658 | 2.889 | 4.133 | 4.481 |

## 4. Cold vs. Persistent Connection Comparison (N = 20 each)

- **Cold Connection (New TCP Handshake per Request):** Mean=`15.290 ms`, P50=`15.548 ms`, P95=`28.287 ms`
- **Warm Connection (Persistent Session Reused):** Mean=`2.089 ms`, P50=`1.806 ms`, P95=`3.082 ms`
- **TCP Handshake / Connection Setup Overhead:** `13.201 ms`

## 5. Outlier Analysis

### Centralized
- Min: `1.025 ms`, Max: `2.462 ms`
- P50: `1.352 ms`, P95: `1.855 ms`, P99: `2.251 ms`
- Requests > 50 ms: `0` / 300 (0.0%)
- Requests > 100 ms: `0` / 300 (0.0%)

### EdgeSync Local
- Min: `1.134 ms`, Max: `5.501 ms`
- P50: `1.609 ms`, P95: `2.267 ms`, P99: `2.664 ms`
- Requests > 50 ms: `0` / 300 (0.0%)
- Requests > 100 ms: `0` / 300 (0.0%)

### EdgeSync Cross-Region
- Min: `1.23 ms`, Max: `4.605 ms`
- P50: `2.929 ms`, P95: `3.936 ms`, P99: `4.526 ms`
- Requests > 50 ms: `0` / 300 (0.0%)
- Requests > 100 ms: `0` / 300 (0.0%)

## 6. Automated Validation Verification

- [x] N = 100 measured requests per architecture per trial (`True`)
- [x] 300 measured observations per trial (`True`)
- [x] 900 total measured observations (`True`)
- [x] Identical request IDs across architectures (`True`)
- [x] Zero warm-up observations mixed into statistics (`True`)
- [x] Workload SHA-256 hash identical across trials (`391bac7738c3a0b2b302febadd221936aea10b92f26bda6cc3dd048b4dd7ff85`)
- [x] No duplicate request IDs within any trial/config (`True`)
- [x] All regional services verified healthy on IPv4 loopback (`127.0.0.1`)

## 7. Key Findings & Final Report

1. **Centralized:** P50=`1.352 ms`, P95=`1.855 ms`, P99=`2.251 ms`
2. **EdgeSync Local:** P50=`1.609 ms`, P95=`2.267 ms`, P99=`2.664 ms`
3. **EdgeSync Cross-Region:** P50=`2.929 ms`, P95=`3.936 ms`, P99=`4.526 ms`
4. **System Latency Comparison:** Centralized system mean=`0.082 ms`, EdgeSync Local=`0.092 ms`, EdgeSync Cross=`0.101 ms`
5. **Inter-Service Communication Overhead:** Local loopback inter-service REST overhead is P50=`1.444 ms`, Mean=`1.011 ms`
6. **Cold vs Persistent Connection Overhead:** Cold connections add `13.201 ms` on average due to TCP socket creation
7. **Outlier Counts:** Total requests >50ms across 900 observations = `0` (0.0% > 100ms)
8. **Trial-to-Trial Consistency:** P50 latencies across Trials 1, 2, 3 vary by < 0.5 ms
9. **Failures/Timeouts:** 0 failed requests, 0 timeouts (100% success rate across 900 measured requests)
10. **Exact Raw Files Generated:**
    - `results/smoke_test/controlled_latency/trial_1_raw.csv`
    - `results/smoke_test/controlled_latency/trial_2_raw.csv`
    - `results/smoke_test/controlled_latency/trial_3_raw.csv`
    - `results/smoke_test/controlled_latency/summary.json`
    - `results/smoke_test/controlled_latency/CONTROLLED_LATENCY_REPORT.md`
