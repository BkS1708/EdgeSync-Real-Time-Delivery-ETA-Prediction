# 🚚 EdgeSync ETA – Distributed Delivery Simulation System

A distributed systems project that simulates real-time delivery ETA prediction across multiple regions using microservices, gossip protocol, and dynamic traffic modeling.

---

## 📌 Overview

EdgeSync ETA is a **distributed ETA prediction system** inspired by real-world platforms like Swiggy and Zomato.

The system divides a city (Mumbai) into multiple regions:
- EAST
- WEST
- CENTRAL

Each region runs as an independent microservice and collaboratively computes delivery time using:
- Distance-based estimation
- Traffic modeling
- Distributed communication
- Gossip protocol for synchronization

---

## ⚙️ Features

### 🌍 Distributed Architecture
- Separate services for EAST, WEST, CENTRAL
- Each node computes ETA independently
- Inter-region communication via REST APIs

### ⏱️ Realistic ETA Calculation
- Haversine distance (real-world distance)
- Speed-based time estimation
- Pickup + Preparation + Delivery breakdown

### 🚦 Traffic Simulation
- Manual traffic selection (Low / Medium / High)
- Optional time-based fallback
- Consistent traffic propagation across nodes

### 🔄 Gossip Protocol
- Nodes share average ETA periodically
- Weighted averaging using sample count
- Simulates decentralized data synchronization

### 🗺️ Interactive UI
- Click-based source & destination selection
- Real-time ETA computation
- Visual breakdown of delivery stages
- Live gossip logs

---

## 🏗️ Project Structure
```bash
EdgeSync-ETA/
│
├── east.py # EAST region service
├── west.py # WEST region service
├── central.py # CENTRAL region service
│
├── utils.py # Core logic (distance, traffic, ETA)
├── config.py # Region mapping
│
├── ui.py # Streamlit frontend
│
├── requirements.txt
└── README.md
```

## 🚀 How to Run

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Start backend services (3 terminals)
```bash
# EAST
uvicorn east:app --port 8000
# WEST
uvicorn west:app --port 9000
# CENTRAL
uvicorn central:app --port 10000
```
### 3️⃣ Run frontend
```bash
streamlit run ui.py
```

### ETA Formula
```bash
ETA = max(Pickup Time, Preparation Time) + Delivery Time
Delivery Time = Distance / Speed (based on traffic)
```
### 🧠 How It Works
- User selects source & destination on map
- Request goes to source region
- Pickup + preparation handled locally
- Delivery handled by destination region
- Traffic factor applied consistently
- ETA = max(pickup, prep) + delivery
- Gossip protocol syncs average ETA across nodes
