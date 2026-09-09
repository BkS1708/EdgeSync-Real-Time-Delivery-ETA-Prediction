# EdgeSync — Smoke Test Validation Report

**Execution Date/Time:** `2026-08-25 08:53:18`  
**Status:** `SUCCESS`  

---

## 1. Did latency test complete?
Yes

## 2. Number of EdgeSync requests
20

## 3. Number of Centralized requests
20

## 4. Number of paired request IDs
20 (intersection of EdgeSync and Centralized request IDs)

## 5. Did scalability complete?
Yes

## 6. Did fault test complete?
Yes

## 7. Did ablation complete?
Yes

## 8. Total execution time
504.58 seconds (8.41 minutes)

### Stage Breakdown:
- **Test 1 (Latency):** 219.73 seconds
- **Test 2 (Scalability):** 123.35 seconds
- **Test 3 (Fault):** 8.41 seconds
- **Test 4 (Ablation):** 139.95 seconds

## 9. Slowest stage
Test 1 (Latency) (219.73s)

## 10. Any errors
None. All stages executed with zero uncaught exceptions.

## 11. Raw files created
- `results/smoke_test/latency/raw_results.csv` (2175 bytes)
- `results/smoke_test/latency/summary.json` (1310 bytes)
- `results/smoke_test/scalability/raw_results.csv` (207 bytes)
- `results/smoke_test/fault/raw_results.csv` (1650 bytes)
- `results/smoke_test/ablation/raw_results.csv` (2073 bytes)
