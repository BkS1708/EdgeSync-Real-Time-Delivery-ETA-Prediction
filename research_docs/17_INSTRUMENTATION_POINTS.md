# EdgeSync Research Dossier: Code Instrumentation Points

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `17_INSTRUMENTATION_POINTS.md`

---

## 1. Overview of Instrumentation Strategy

To measure latency, computation vs network time breakdown, gossip convergence delay, and throughput metrics without altering core application logic, explicit metric collection hooks must be inserted. This document identifies the exact source files, function names, and line ranges where instrumentation should be added.

---

## 2. Core Code Instrumentation Points

### Point 1: Request Processing & End-to-End Decision Latency Timer

```text
File: east.py (and west.py, central.py)
function/class: custom_eta(data: dict)
line numbers: Lines 19-20 (Entry point) and Line 68 (Exit point)
purpose: Measure total end-to-end server processing time for /custom_eta requests.
relevant behavior: Insert high-resolution timer start = time.perf_counter() at L20, measure duration = (time.perf_counter() - start) * 1000 at L68, append to latency telemetry buffer.
```

**Proposed Instrumentation Snippet:**
```python
# Insert at east.py:L20
t_start = time.perf_counter()

# ... existing calculation logic ...

# Insert at east.py:L68
t_total_ms = (time.perf_counter() - t_start) * 1000.0
# Log t_total_ms to CSV or Prometheus metric exporter
```

---

### Point 2: Cross-Region Inter-Service Network Call Timer

```text
File: east.py (and west.py, central.py)
function/class: custom_eta(data: dict)
line numbers: Lines 52-56
purpose: Measure network round-trip latency incurred when calling remote region /calc_delivery REST API.
relevant behavior: Measure t_net_start = time.perf_counter() before requests.post(), compute net_duration_ms after response returned. Isolates network delegation overhead from local math computation.
```

**Proposed Instrumentation Snippet:**
```python
# Insert before east.py:L52
t_net_start = time.perf_counter()
res = requests.post(url_map[dest_region], json={...}).json()
t_net_ms = (time.perf_counter() - t_net_start) * 1000.0
```

---

### Point 3: Remote Delivery Computation Execution Timer

```text
File: east.py (and west.py, central.py)
function/class: calc_delivery(data: dict)
line numbers: Lines 79-94
purpose: Measure processing time of remote delivery leg calculation on the destination node.
relevant behavior: Record execution time of distance() + estimate_time_from_distance() on destination microservice.
```

---

### Point 4: Gossip Outbound Send & Network Transmission Timer

```text
File: east.py (and west.py, central.py)
function/class: gossip()
line numbers: Lines 101-104
purpose: Measure HTTP POST gossip send latency and track control payload byte volume.
relevant behavior: Record time taken for requests.post("http://localhost:9000/sync", json=state) and record payload size sys.getsizeof(json.dumps(state)).
```

---

### Point 5: Gossip Sync Receiver & Merge Processing Timer

```text
File: east.py (and west.py, central.py)
function/class: sync(data: dict)
line numbers: Lines 114-132
purpose: Measure execution time of sample-weighted average merge algorithm and log incoming vs outgoing state divergence.
relevant behavior: Insert timer around lines 120-128; log delta_avg = abs(state['avg_eta'] - incoming_avg).
```

---

### Point 6: Process-Level CPU & RAM Hardware Monitor

```text
File: east.py (and west.py, central.py)
function/class: Background Process Monitor (New helper thread)
line numbers: Global module level (e.g. east.py:L112)
purpose: Continuously record CPU utilization (%), Resident Set Size (RSS Memory in MB), and thread count per FastAPI node process using psutil.
```

---

## 3. Telemetry Exporter Blueprint

Create a dedicated lightweight metric collector utility `utils_telemetry.py` that can be imported by all microservices:

```python
# utils_telemetry.py (Proposed New File)
import time, psutil, os, csv

class MetricCollector:
    def __init__(self, region_name):
        self.region = region_name
        self.process = psutil.Process(os.getpid())
        
    def record_request(self, endpoint, total_ms, net_ms=0.0):
        # Writes [timestamp, region, endpoint, total_ms, net_ms, cpu%, ram_mb] to CSV
        pass
```
