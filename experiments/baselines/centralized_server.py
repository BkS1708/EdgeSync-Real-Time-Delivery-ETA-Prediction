# ========================= centralized_server.py =========================

from fastapi import FastAPI
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

app = FastAPI(title="EdgeSync Baseline - Centralized Cloud Server")

obs_store = ObservationStore()
start_time = time.time()

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "mode": "centralized",
        "uptime_seconds": time.time() - start_time
    }

@app.post("/custom_eta")
def custom_eta(data: dict):
    t_start = time.perf_counter()
    source = data["source"]
    dest = data["destination"]
    food = data["food"]
    rider_option = data["rider"]

    # Pickup + Preparation (All computed at Centralized Cloud Server)
    pickup = get_rider_distance_from_option(rider_option) * 2
    prep = get_prep_time(food)

    # Dynamic Traffic
    traffic_level = data.get("traffic")
    if not traffic_level:
        traffic_level = dynamic_traffic()

    # Delivery Leg (Computed locally at Centralized Cloud Server - no regional delegation)
    delivery = estimate_time_from_distance(
        distance(source, dest),
        traffic_level
    )

    ETA = max(pickup, prep) + delivery

    # Record Observation
    obs = Observation(origin_region="CENTRALIZED", eta=ETA)
    obs_store.add_observation(obs.to_dict())

    t_total_ms = (time.perf_counter() - t_start) * 1000.0

    return {
        "obs_id": obs.obs_id,
        "ETA": ETA,
        "pickup": pickup,
        "prep": prep,
        "delivery": delivery,
        "traffic": traffic_level,
        "source_region": "CENTRALIZED",
        "dest_region": "CENTRALIZED",
        "latency_ms": {
            "total": t_total_ms,
            "network": 0.0,
            "computation": t_total_ms
        }
    }
