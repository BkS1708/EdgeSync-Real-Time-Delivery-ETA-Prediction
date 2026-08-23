# EdgeSync Research Dossier: Data & Dataset Analysis

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `18_DATA_AND_DATASET_ANALYSIS.md`

---

## 1. Repository Data Audit

A complete search across all directory files in `EdgeSync-ETA-main` was conducted to locate datasets, empirical log files, historical trip telemetry, test scenarios, or measurement records.

### Audit Summary Table

| Data Category | Found in Repository? | File Path / Location | Assessment & Description |
| :--- | :--- | :--- | :--- |
| **Real World Trip Datasets** | **NO** | N/A | No real delivery order dataset (e.g. Swiggy, Zomato, Uber Movement) exists in the repository. |
| **Synthetic Input Queries** | **PARTIAL** | [`ui.py:L27`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/ui.py#L27) | Single default map center coordinate `[19.0760, 72.8777]` (Mumbai center). No pre-recorded test query suite. |
| **System Event Logs** | **PARTIAL** | In-memory `logs` list in [`east.py:L11`](file:///d:/Desktop/NM-Notes%20anf%20Files/EdgeSync_Research%20Paper/Project_Files/EdgeSync-ETA-main/EdgeSync-ETA-main/east.py#L11) | Strings generated dynamically during runtime. Wiped on process exit; not persisted to disk. |
| **Performance Measurements** | **NO** | N/A | Zero latency records, CPU logs, RAM logs, or bandwidth traces in repository (**`NOT IMPLEMENTED`**). |
| **Trained ML Models / Weights**| **NO** | N/A | No `.pkl`, `.onnx`, or `.pt` model files in repository. |
| **Geospatial Road Network Data**| **NO** | N/A | Uses straight-line Haversine math; no OpenStreetMap (`.osm`) or shapefile network data included. |

---

## 2. Evaluation Sufficiency Assessment

**Verdict: INSUFFICIENT DATA FOR IEEE PERCOM SUBMISSION**

The current repository lacks sufficient data, pre-recorded inputs, or benchmarks to generate the quantitative graphs, statistical tables, and comparative evaluation required by IEEE PerCom reviewers.

---

## 3. Required Dataset & Data Collection Plan

To prepare the repository for rigorous PerCom evaluation, we must collect/generate three datasets:

### Dataset 1: Synthesized Mumbai Delivery Query Workload (`data/mumbai_delivery_requests.json`)
- **Description:** A dataset of 10,000 synthetic food delivery orders distributed across Mumbai coordinates.
- **Fields Required:** `order_id`, `source_lat`, `source_lon`, `dest_lat`, `dest_lon`, `food_item`, `rider_option`, `traffic_level`, `timestamp`.
- **Generation Method:** Sample source coordinates from restaurant clusters in Powai, Bandra, Lower Parel, Andheri; sample destination coordinates within 1-20 km radii.

### Dataset 2: Real-World Traffic Speed Benchmark Dataset (`data/mumbai_traffic_speeds.csv`)
- **Description:** Speed observations across Mumbai corridors (e.g. Western Express Highway, LBS Marg) to validate travel speed maps.
- **Data Source:** Extract open traffic speeds from Uber Movement or TomTom Traffic Stats for Mumbai.

### Dataset 3: Measured System Performance Logs (`data/benchmarks/`)
- **Description:** Output CSV files generated during experimental execution of Experiments A through I.
- **Required Files:**
  - `latency_benchmarks.csv` (Timestamp, Region, Endpoint, Total_ms, Net_ms)
  - `gossip_divergence.csv` (Timestamp, East_Avg, West_Avg, Central_Avg)
  - `resource_utilization.csv` (Timestamp, Node, CPU_Pct, RAM_MB)
