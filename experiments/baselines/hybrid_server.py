# ========================= hybrid_server.py =========================

from fastapi import FastAPI
import requests
import time
from utils import (
    distance,
    estimate_time_from_distance,
    dynamic_traffic,
    get_rider_distance_from_option,
    get_prep_time,
    Observation,
    ObservationStore
)

app = FastAPI(title="EdgeSync Baseline - Hybrid Central Cloud Server")
obs_store = ObservationStore()
start_time = time.time()

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "mode": "hybrid_cloud",
        "uptime_seconds": time.time() - start_time
    }

# Central Cloud Delivery Leg Endpoint for Hybrid Mode
@app.post("/calc_delivery")
def calc_delivery(data: dict):
    source = data["source"]
    dest = data["dest"]
    traffic_level = data.get("traffic")

    if not traffic_level:
        traffic_level = dynamic_traffic()

    delivery = estimate_time_from_distance(
        distance(source, dest),
        traffic_level
    )

    return {"delivery_time": delivery}
