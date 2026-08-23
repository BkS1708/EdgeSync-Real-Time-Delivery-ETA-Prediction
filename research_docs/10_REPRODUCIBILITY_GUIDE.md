# EdgeSync Research Dossier: Reproducibility & Deployment Guide

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `10_REPRODUCIBILITY_GUIDE.md`

---

## 1. Prerequisites & Environment Specifications

- **Operating System:** Windows 10/11, Ubuntu 20.04/22.04 LTS, or macOS 12+
- **Python Runtime:** Python `3.9`, `3.10`, or `3.11`
- **Network Interface:** Localhost network interface allowing TCP ports `8000`, `9000`, `10000`, and `8501`.

---

## 2. Step-by-Step Installation

1. **Clone / Open Repository Directory:**
   ```bash
   cd "d:\Desktop\NM-Notes anf Files\EdgeSync_Research Paper\Project_Files\EdgeSync-ETA-main\EdgeSync-ETA-main"
   ```

2. **Create Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```
   *Dependencies installed:* `fastapi`, `uvicorn`, `streamlit`, `folium`, `streamlit-folium`, `matplotlib`, `requests`.

---

## 3. System Startup Instructions

### Step 1: Launch Regional Microservice Nodes (3 Separate Terminals)

**Terminal 1 (EAST Node - Port 8000):**
```bash
uvicorn east:app --port 8000 --reload
```

**Terminal 2 (WEST Node - Port 9000):**
```bash
uvicorn west:app --port 9000 --reload
```

**Terminal 3 (CENTRAL Node - Port 10000):**
```bash
uvicorn central:app --port 10000 --reload
```

### Step 2: Launch Streamlit Frontend (Terminal 4)
```bash
streamlit run ui.py
```
*Access the web UI at:* `http://localhost:8501`

---

## 4. API Testing & Curl Verification Suite

### Test 1: Intra-Region Custom ETA Request (EAST $\rightarrow$ EAST)
```bash
curl -X POST "http://localhost:8000/custom_eta" \
     -H "Content-Type: application/json" \
     -d '{
           "source": [19.1197, 72.9050],
           "destination": [19.1300, 72.9150],
           "food": "pizza",
           "rider": "Near (0.5-2 km)",
           "traffic": "High"
         }'
```
*Expected Response:* `{"ETA": ..., "pickup": ..., "prep": ..., "delivery": ..., "traffic": "High"}`

---

### Test 2: Cross-Region Custom ETA Request (EAST $\rightarrow$ WEST Delegation)
```bash
curl -X POST "http://localhost:8000/custom_eta" \
     -H "Content-Type: application/json" \
     -d '{
           "source": [19.1197, 72.9050],
           "destination": [19.0596, 72.8295],
           "food": "burger",
           "rider": "Far (5-8 km)",
           "traffic": "Medium"
         }'
```
*Expected Response:* Triggers internal POST from port 8000 to `http://localhost:9000/calc_delivery` and aggregates total ETA.

---

### Test 3: Inspect Microservice Gossip Logs
```bash
curl -X GET "http://localhost:8000/logs"
```
*Expected Response:* `{"logs": ["EAST → Sent avg ...", "EAST ← Received avg ..."]}`

---

## 5. Known Reproduction Gotchas & Execution Fixes

1. **Food Category Case-Sensitivity:**  
   When invoking `/custom_eta` via `curl` or UI, pass lowercase food strings (`"pizza"`, `"burger"`, `"sandwich"`, `"taco"`) to avoid falling back to the default prep time range.
2. **Missing Port Startup:**  
   If you try to compute an ETA from `EAST` to `WEST` before starting `west.py`, `east.py` will fail with `requests.exceptions.ConnectionError`. Ensure **all three** server ports (`8000`, `9000`, `10000`) are running before submitting requests.
3. **Random Seed Initialization:**  
   Because `random.uniform(0.9, 1.1)` is unseeded, consecutive requests with identical inputs will yield slightly varying ETA values (±10%). Set `random.seed(42)` in `utils.py` if exact deterministic outputs are required.
