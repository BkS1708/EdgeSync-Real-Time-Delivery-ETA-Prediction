# EdgeSync Research Dossier: Project Overview

**Target Conference:** IEEE PerCom 2027 (25th IEEE International Conference on Pervasive Computing and Communications)  
**Analysis Date:** August 2026  
**Repository Path:** `d:\Desktop\NM-Notes anf Files\EdgeSync_Research Paper\Project_Files\EdgeSync-ETA-main\EdgeSync-ETA-main`  
**Paper Source Analyzed:** `EdgeSyncETA_Final.doc` (located in parent workspace directory)

---

## 1. Project Summary

**EdgeSync** is a distributed delivery Estimated Time of Arrival (ETA) simulation framework designed for modern urban metropolitan areas, specifically parameterized for Mumbai, India. The system partitions the geographic area of the city into three distinct regional zones—**EAST**, **WEST**, and **CENTRAL**—and runs an independent FastAPI microservice process for each region on dedicated HTTP ports (`8000`, `9000`, and `10000` respectively).

When a user submits a food delivery request via an interactive Streamlit UI, the system routes the request to the source region's microservice. The source node estimates rider pickup time and restaurant preparation time locally, determines whether the delivery destination lies in the same region or a peer region, and delegates destination travel estimation across regions via REST HTTP requests if necessary. Additionally, each regional node runs a background daemon thread that periodically exchanges local aggregated ETA statistics with a peer node using a 3-node gossip ring topology to maintain global state synchronization.

---

## 2. Problem Being Solved

Food delivery platforms operating in dense metropolitan environments (such as Swiggy and Zomato in Mumbai) struggle with accurate, low-latency ETA estimations due to:
1. **Severe Traffic Variability:** Intra-city speeds fluctuate dramatically based on time-of-day peak congestion and localized weather/infrastructure disruptions.
2. **Centralized Architectural Bottlenecks:** Routing all spatial queries and status updates to a single centralized cloud data center introduces network latency, single-point-of-failure vulnerabilities, and unnecessary cross-boundary data transfers when the order origin and destination are physically co-located in the same neighborhood.
3. **Regional Disconnects:** Purely localized edge models without cross-node synchronization lack a global view of city-wide delivery trends and traffic impacts across zone boundaries.

EdgeSync addresses this by combining **regionally partitioned edge microservices**, **cross-region REST delegation**, and **gossip-based asynchronous state synchronization**.

---

## 3. Core Research Idea

The core research premise of EdgeSync is that **geographic edge partitioning of urban ETA computations reduces decision latency and isolates regional traffic dynamics while maintaining global statistical awareness through decentralized gossip protocols.**

Key architectural principles implemented:
- **Spatial Locality:** Requests originating in a region are processed by that region's local edge service.
- **Distributed Delegation:** When a delivery crosses regional boundaries, the destination leg calculation is executed by the destination edge node.
- **Decentralized Synchronization:** Regional nodes continuously aggregate observed ETAs and propagate weighted running averages across a peer-to-peer gossip ring without a centralized broker.

---

## 4. Complete Technology Stack

The actual implementation in the repository relies on the following tech stack:

| Category | Technology / Library | Version / Requirement | Source / Evidence |
| :--- | :--- | :--- | :--- |
| **Programming Language** | Python | 3.9+ | [`requirements.txt`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/requirements.txt) |
| **Microservice Framework** | FastAPI | Listed in requirements | [`east.py:L3`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L3), [`west.py:L3`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/west.py#L3), [`central.py:L3`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/central.py#L3) |
| **ASGI Web Server** | Uvicorn | Listed in requirements | [`README.md:L82-L86`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/README.md#L82-L86), [`Server Commands.txt`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/Server%20Commands.txt) |
| **HTTP Client Library** | Requests | Listed in requirements | Inter-node REST API calls & gossip sync in microservices |
| **Frontend Framework** | Streamlit | Listed in requirements | [`ui.py:L3`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/ui.py#L3) |
| **Geospatial Visualization**| Folium & `streamlit-folium` | Listed in requirements | [`ui.py:L4-L5`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/ui.py#L4-L5) (Interactive Mumbai Map) |
| **Data Plotting** | Matplotlib | Listed in requirements | [`ui.py:L8`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/ui.py#L8) (Bar charts of ETA breakdown) |
| **Concurrency Mechanism** | Standard Library `threading` | Native Python | Background gossip daemon threads in `east.py`, `west.py`, `central.py` |
| **Geospatial Math** | Math / Trigonometry | Native Python | Haversine distance formula in [`utils.py:L6-L17`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/utils.py#L6-L17) |
| **Database / Storage** | None | **NOT IMPLEMENTED** | In-memory dictionary state only |
| **Machine Learning** | None | **NOT IMPLEMENTED** | Heuristic formula & random sampling only |

---

## 5. Repository Structure

```text
EdgeSync-ETA-main/
├── README.md              # High-level overview, architecture summary, and run instructions
├── Server Commands.txt    # Shell commands to start microservices with uvicorn
├── requirements.txt       # Python package dependencies
├── config.py              # Spatial partitioning logic (get_region)
├── utils.py               # Haversine distance, speed model, dynamic traffic, prep time, rider distance
├── east.py                # FastAPI microservice for EAST region (Port 8000) + Gossip sender to WEST
├── west.py                # FastAPI microservice for WEST region (Port 9000) + Gossip sender to CENTRAL
├── central.py             # FastAPI microservice for CENTRAL region (Port 10000) + Gossip sender to EAST
└── ui.py                  # Streamlit interactive user interface & Folium map renderer
```

### Detailed File Roles & Evidence

```text
File: config.py
function/class: get_region(lat, lon)
purpose: Classifies a geographic coordinate into CENTRAL, WEST, or EAST.
relevant behavior: Lat < 19.05 -> CENTRAL; Lon < 72.85 -> WEST; else -> EAST.
```

```text
File: utils.py
function/class: distance(p1, p2), estimate_time_from_distance(), dynamic_traffic(), get_rider_distance_from_option(), get_prep_time()
purpose: Holds core physical and mathematical heuristics for ETA computation.
relevant behavior: Computes Haversine distance (km), maps traffic levels to speed (35/25/15 km/h), samples prep times and rider distance with uniform noise.
```

```text
File: east.py / west.py / central.py
function/class: FastAPI app, custom_eta(), calc_delivery(), gossip(), sync(), get_logs()
purpose: Implements independent regional edge node servers.
relevant behavior: Handles local ETA estimation, delegates cross-region delivery via REST, runs background gossip thread every 5s, updates weighted avg state.
```

```text
File: ui.py
function/class: Streamlit app layout, create_map(), st_folium handler, REST triggers
purpose: Provides visual frontend for user interaction.
relevant behavior: Captures click coordinates for source/dest, triggers local source microservice, displays ETA component chart and live gossip logs.
```

---

## 6. Execution Architecture

The startup and communication flow during execution is depicted below:

1. **Service Initialization:**
   - Three independent Uvicorn processes start:
     - `east.py` listening on `http://localhost:8000`
     - `west.py` listening on `http://localhost:9000`
     - `central.py` listening on `http://localhost:10000`
   - Upon module load, each process spawns a daemon thread running `gossip()`.

2. **Frontend Launch:**
   - Streamlit starts `ui.py` on default port `8501`.
   - The user opens the web browser and selects two points on the Folium map (Source, Destination) and options (Food, Rider Proximity, Traffic).

3. **Request Flow:**
   - `ui.py` invokes `config.get_region(src_lat, src_lon)` locally to find `src_region`.
   - `ui.py` sends HTTP POST to `http://localhost:<src_port>/custom_eta`.
   - The receiving node (e.g., `east.py`) computes local pickup and prep times.
   - `east.py` checks `dest_region = get_region(dest_lat, dest_lon)`.
     - If `dest_region == "EAST"`: `east.py` computes delivery time locally.
     - If `dest_region == "WEST"`: `east.py` issues HTTP POST to `http://localhost:9000/calc_delivery`.
   - `east.py` computes `ETA = max(pickup, prep) + delivery`, updates local state, and returns JSON to `ui.py`.

4. **Gossip Synchronization Ring:**
   - `east.py` sends `POST http://localhost:9000/sync` every 5 seconds.
   - `west.py` sends `POST http://localhost:10000/sync` every 5 seconds.
   - `central.py` sends `POST http://localhost:8000/sync` every 5 seconds.

---

## 7. Current Maturity Level

**Classification: Proof-of-Concept (PoC) / Academic Prototype**

### Justification:
1. **Hardcoded Ports & Localhost Networking:** Inter-service URLs (`http://localhost:8000`, etc.) are hardcoded directly inside microservice source files ([`east.py:L47-L49`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L47-L49)). There is no environment-based configuration, container orchestration, or dynamic service discovery.
2. **In-Memory Volatile State:** Microservice state (`avg_eta`, `samples`, `logs`) is stored in Python in-memory dictionaries and lists ([`east.py:L11-L16`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L11-L16)). Restarting a process wipes out all state.
3. **Formula-Based Heuristics:** There are no trained Machine Learning models (such as LightGBM, GNNs, or XGBoost) or real-world sensor data feeds.
4. **Lack of Automated Testing & Metrics:** There are no unit tests, integration tests, latency benchmarking scripts, or performance evaluation suites in the repository (**`IMPLEMENTED BUT NOT QUANTITATIVELY EVALUATED`**).
