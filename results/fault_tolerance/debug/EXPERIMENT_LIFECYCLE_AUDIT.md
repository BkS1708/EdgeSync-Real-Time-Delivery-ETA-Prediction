# EdgeSync Fault-Tolerance — Experiment Lifecycle Audit

**Audit Date/Time:** `2026-08-25 18:00:00`  
**Focus:** Lifecycle management, process orchestration, state isolation, and fault reset mechanisms.

---

## 1. Documented Lifecycle Progression

The intended experimental execution lifecycle follows this sequential state machine:

```
[ START ]
   │
   ▼
[ HEALTH CHECK & SERVICE INITIALIZATION ]
   │  Ensure EAST (8000), WEST (9000), CENTRAL (10000) are online
   │  Reset partition flags and clear network emulation parameters
   ▼
[ BASELINE PHASE (Req 1–50) ]
   │  Normal operation across healthy topology
   ▼
[ FAILURE INJECTION (Req 51) ]
   │  Record failure_injection_timestamp
   │  Trigger fault (Process Kill / /partition API / Packet Loss)
   ▼
[ FAILURE PHASE (Req 51–150) ]
   │  Workload continues through failure window
   │  Measure detection latency and local fallback invocation
   ▼
[ FAULT REMOVAL / RESTORATION (Req 151) ]
   │  Record failure_recovery_timestamp
   │  Restart process / Call /unpartition API / Clear packet loss
   ▼
[ RECOVERY PHASE (Req 151–200) ]
   │  Workload continues with restored network/node
   │  Measure first normal non-fallback request latency
   ▼
[ CONVERGENCE & SYNC POLLING ]
   │  Poll /state across EAST, WEST, CENTRAL every 200 ms
   │  Measure time_to_first_sync and time_to_full_convergence
   ▼
[ CLEANUP & TEARDOWN ]
   │  Persist trial raw CSV
   │  Reset cluster state for next trial
```

---

## 2. Audit of Lifecycle Components

### 2.1 Service Startup & Process Management
- **Implementation:** `ClusterManager.start_node(region_name)` spawns Uvicorn via `subprocess.Popen([py_exec, "-m", "uvicorn", f"{region.lower()}:app", "--port", ...])`.
- **Readiness Handshake:** Polls `GET /health` with a timeout of 0.5s up to 20 attempts ($\approx 4\text{ s}$ total window).
- **Finding:** Startup and health checks work reliably when the application code itself starts cleanly.

### 2.2 Process Termination & Port Cleanup
- **Implementation:** `ClusterManager.kill_node(region_name)` terminates the `Popen` process handle, waits 2.0s, falls back to `kill()`, and on Windows executes a fallback `taskkill /f /pid <pid>` by scanning `netstat -aon`.
- **Finding:** Reliable on Windows; no orphan listeners remained bound to ports 8000, 9000, or 10000.

### 2.3 Network Partition & Emulation Reset
- **Implementation:**
  - Transport partition is controlled via `@app.post("/partition")` and `@app.post("/unpartition")`, maintaining a `blocked_peers` set in the FastAPI application.
  - When partitioned, outgoing HTTP requests to blocked peers immediately raise `requests.exceptions.ConnectionError`.
  - At the start of each trial, `ClusterManager` calls `/unpartition` on all 3 nodes.
- **Finding:** Reset mechanism works as designed when the node is reachable.

### 2.4 State Isolation Between Trials
- **Observation Store Volatility:** The `ObservationStore` in `east.py`, `west.py`, `central.py` is held in in-memory global state (`obs_store = ObservationStore()`).
- **Audit Finding:**
  - In scenarios where nodes are **not restarted** between trials (e.g., `scenario_3`, `scenario_4`, `scenario_5`), observations from trial 1 remained in the in-memory `obs_store` into trial 2 and trial 3 because no explicit `/reset_state` endpoint was invoked between trials.
  - While request-level latency is independent, observation count accumulated across trials within the same process lifecycle unless the process was restarted.
  - **Recommendation:** Add a `@app.post("/reset")` endpoint to clear `obs_store.observations` between experimental trials.

---

## 3. Root-Cause Analysis of Trial Execution Failures

The lifecycle audit revealed that the collapse of scenarios 3, 4, 5 and parts of 2 and 6 was **not caused by lifecycle orchestration failures or hanging subprocesses**, but by an unhandled signature mismatch:
- `east.py` called `dest_region = get_region(dest)`.
- `config.get_region(lat, lon)` expected two positional arguments.
- Because `dest` was passed as `[lat, lon]`, FastAPI raised an uncaught `TypeError` on every incoming request to `/custom_eta`.
- Consequently, requests failed before reaching the baseline/failure/recovery logic, resulting in 200 HTTP 500 errors in those raw files.
