# EdgeSync Research Dossier: API & Microservice Analysis

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `02_API_AND_MICROSERVICE_ANALYSIS.md`

---

## 1. Overview of Microservice Endpoints

The EdgeSync framework consists of three identical FastAPI instances (`east.py`, `west.py`, `central.py`). Each instance exposes **four HTTP endpoints**. There are no distinct or specialized endpoints on any single node; all nodes implement the exact same set of 4 APIs.

---

## 2. Comprehensive Endpoint Catalog

### Endpoint 1: `/custom_eta`

```text
File: east.py / west.py / central.py
function/class: custom_eta(data: dict)
line range: Lines 19-74
```

- **HTTP Method:** `POST`
- **Path:** `/custom_eta`
- **Purpose:** Primary end-to-end delivery ETA computation endpoint. Invoked by the client frontend (`ui.py`). Computes local rider pickup time, restaurant preparation time, and delivery travel time (locally or cross-region). Updates the local node's running average ETA state.
- **Request Schema (JSON):**
  ```json
  {
    "source": [19.1197, 72.9050],
    "destination": [19.0596, 72.8295],
    "food": "Pizza",
    "rider": "Near (0.5-2 km)",
    "traffic": "High"
  }
  ```
  - `source` (list of float, required): `[latitude, longitude]` of pickup location.
  - `destination` (list of float, required): `[latitude, longitude]` of drop-off location.
  - `food` (string, required): Options: `"Pizza"`, `"Burger"`, `"Sandwich"`, `"Taco"`.
  - `rider` (string, required): Proximity range string: `"Near (0.5-2 km)"`, `"Medium (2-5 km)"`, `"Far (5-8 km)"`.
  - `traffic` (string, optional): Traffic level override: `"Low"`, `"Medium"`, `"High"`. Defaults to `dynamic_traffic()` if omitted/empty.
- **Response Schema (JSON):**
  ```json
  {
    "ETA": 38.42,
    "pickup": 2.64,
    "prep": 7.50,
    "delivery": 30.92,
    "traffic": "High"
  }
  ```
- **Internal Functions Called:**
  - `config.get_region(dest[0], dest[1])` ([`config.py:L1-L7`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/config.py#L1-L7))
  - `utils.get_rider_distance_from_option(rider_option)` ([`utils.py:L42-L50`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L42-L50))
  - `utils.get_prep_time(food)` ([`utils.py:L53-L62`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L53-L62))
  - `utils.dynamic_traffic()` ([`utils.py:L31-L39`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L31-L39))
  - `utils.distance(source, dest)` ([`utils.py:L6-L17`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L6-L17))
  - `utils.estimate_time_from_distance(distance, traffic)` ([`utils.py:L20-L28`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L20-L28))
- **External Network Calls:**
  - If `dest_region != current_region`, calls `requests.post(url_map[dest_region], json={...})` to the destination node's `/calc_delivery` endpoint.
- **Execution Mode:** Synchronous (def endpoint in FastAPI).
- **State Modification:** Modifies global dictionary `state`:
  ```python
  state["samples"] += 1
  state["avg_eta"] = ((state["avg_eta"] * (state["samples"] - 1)) + ETA) / state["samples"]
  ```
- **Error Handling:** **None**. Missing dictionary keys or failed HTTP requests to peer nodes raise raw Python exceptions (`KeyError`, `requests.exceptions.ConnectionError`).

---

### Endpoint 2: `/calc_delivery`

```text
File: east.py / west.py / central.py
function/class: calc_delivery(data: dict)
line range: Lines 78-94
```

- **HTTP Method:** `POST`
- **Path:** `/calc_delivery`
- **Purpose:** Regional delivery calculation endpoint. Computes travel time for the delivery leg when a remote edge node delegates a cross-region request.
- **Request Schema (JSON):**
  ```json
  {
    "source": [19.1197, 72.9050],
    "dest": [19.0596, 72.8295],
    "traffic": "High"
  }
  ```
- **Response Schema (JSON):**
  ```json
  {
    "delivery_time": 30.92
  }
  ```
- **Internal Functions Called:**
  - `utils.dynamic_traffic()` (if traffic parameter is missing)
  - `utils.distance(source, dest)`
  - `utils.estimate_time_from_distance(distance_km, traffic_level)`
- **External Network Calls:** None.
- **Execution Mode:** Synchronous.
- **State Modification:** None. This endpoint is stateless.
- **Error Handling:** None.

---

### Endpoint 3: `/sync`

```text
File: east.py / west.py / central.py
function/class: sync(data: dict)
line range: Lines 114-132
```

- **HTTP Method:** `POST`
- **Path:** `/sync`
- **Purpose:** Receives gossip synchronization payloads from peer edge nodes and updates the local running average ETA state using weighted averaging.
- **Request Schema (JSON):**
  ```json
  {
    "avg_eta": 28.50,
    "samples": 12
  }
  ```
- **Response Schema (JSON):**
  ```json
  {
    "status": "ok"
  }
  ```
- **State Modification:** Modifies `state` and appends to `logs`:
  ```python
  incoming_avg = data.get("avg_eta", 0)
  incoming_samples = data.get("samples", 1)
  total_samples = state["samples"] + incoming_samples
  if total_samples > 0:
      state["avg_eta"] = ((state["avg_eta"] * state["samples"]) + (incoming_avg * incoming_samples)) / total_samples
      state["samples"] = total_samples
  logs.append(f"{region} ← Received avg {incoming_avg:.2f}")
  ```
- **Execution Mode:** Synchronous.
- **Error Handling:** Safe defaults (`.get("avg_eta", 0)`, `.get("samples", 1)`).

---

### Endpoint 4: `/logs`

```text
File: east.py / west.py / central.py
function/class: get_logs()
line range: Lines 135-137
```

- **HTTP Method:** `GET`
- **Path:** `/logs`
- **Purpose:** Exposes recent gossip event logs to the client UI.
- **Request Schema:** None (URL parameters or query params not required).
- **Response Schema (JSON):**
  ```json
  {
    "logs": [
      "EAST → Sent avg 28.50",
      "EAST ← Received avg 24.12"
    ]
  }
  ```
- **State Modification:** None (returns slice `logs[-10:]`).
- **Execution Mode:** Synchronous.
- **Error Handling:** None needed.

---

## 3. Discrepancies Between Code and Paper Documentation

1. **Missing Endpoints Claimed in Paper:**
   - Section III of `EdgeSyncETA_Final.doc` mentions separate microservices for *Rider Distance Service*, *Restaurant Preparation Service*, *Traffic Analysis Service*, and *ETA Engine*.
   - **Code Reality:** These are **NOT IMPLEMENTED** as distinct microservices or separate endpoints. They exist only as inline function calls inside a monolithic `/custom_eta` endpoint.
2. **Missing Routing & Health Endpoints:**
   - The paper describes cloud routing and health management.
   - **Code Reality:** No `/health`, `/metrics`, or cloud routing endpoints exist anywhere in the codebase (**`NOT IMPLEMENTED`**).
