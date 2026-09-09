# EdgeSync Scalability Experiment — Reproducibility & Environment Specification

**Experiment Date:** `2026-08-25 23:51:18`  
**Execution Host:** `BkS`  
**Operating System:** `Windows-11-10.0.26200-SP0` (`win32`)  
**Python Version:** `3.14.0 (tags/v3.14.0:ebf955d, Oct  7 2025, 10:15:03) [MSC v.1944 64 bit (AMD64)]`  
**CPU Architecture:** `Intel64 Family 6 Model 170 Stepping 4, GenuineIntel` (16 Physical / 22 Logical Cores)  
**System Memory:** `15.43 GB`  

---

## 1. Experimental Configuration & Random Seeds

- **Random Seed (Trial 1):** `101` (Warmup Seed: `801`)
- **Random Seed (Trial 2):** `202` (Warmup Seed: `802`)
- **Random Seed (Trial 3):** `303` (Warmup Seed: `803`)
- **Concurrency Levels:** `[1, 2, 4, 8, 16, 32, 64]`
- **Measured Requests per Condition:** `100`
- **Warmup Requests per Condition:** `20`
- **Cluster Node Endpoints:**
  - EAST Node: `http://127.0.0.1:8000`
  - WEST Node: `http://127.0.0.1:9000`
  - CENTRAL Node: `http://127.0.0.1:10000`
- **Network Stack:** IPv4 Loopback `127.0.0.1` with persistent HTTP/1.1 session pooling (`requests.Session` per thread)

## 2. GPU Utilization Declaration

> GPU acceleration was not used because the scalability workload is dominated by HTTP networking, process scheduling, concurrency, and distributed coordination rather than GPU-computable kernels.

## 3. Rerun Command

To reproduce the complete scalability experiment from scratch:
```bash
python experiments/runners/run_full_scalability_experiment.py
```
