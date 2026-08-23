# ========================= central.py =========================

from fastapi import FastAPI
import requests, time, threading
from utils import *
from config import get_region

app = FastAPI()
region = "CENTRAL"

logs = []

state = {
    "avg_eta": 0,
    "samples": 0
}

# ---------------- CUSTOM ETA ----------------
@app.post("/custom_eta")
def custom_eta(data: dict):

    source = data["source"]
    dest = data["destination"]
    food = data["food"]
    rider_option = data["rider"]

    dest_region = get_region(dest[0], dest[1])

    # Pickup + Preparation
    pickup = get_rider_distance_from_option(rider_option) * 2
    prep = get_prep_time(food)

    # Dynamic Traffic
    traffic_level = data.get("traffic")

    if not traffic_level:
        traffic_level = dynamic_traffic()

    # Distributed Delivery
    if dest_region == region:
        delivery = estimate_time_from_distance(
            distance(source, dest),
            traffic_level
        )
    else:
        url_map = {
            "EAST": "http://localhost:8000/calc_delivery",
            "WEST": "http://localhost:9000/calc_delivery",
            "CENTRAL": "http://localhost:10000/calc_delivery"
        }

        res = requests.post(url_map[dest_region], json={
            "source": source,
            "dest": dest,
            "traffic": traffic_level
        }).json()

        delivery = res["delivery_time"]

    ETA = max(pickup, prep) + delivery

    # -------- Weighted Average Update --------
    state["samples"] += 1
    state["avg_eta"] = (
        (state["avg_eta"] * (state["samples"] - 1)) + ETA
    ) / state["samples"]

    return {
        "ETA": ETA,
        "pickup": pickup,
        "prep": prep,
        "delivery": delivery,
        "traffic": traffic_level
    }


# ---------------- DELIVERY SERVICE ----------------
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


# ---------------- GOSSIP ----------------
def gossip():
    while True:
        try:
            # CENTRAL → EAST
            requests.post("http://localhost:8000/sync", json=state)
            logs.append(f"{region} → Sent avg {state['avg_eta']:.2f}")

        except:
            logs.append(f"{region} → Gossip failed")

        time.sleep(5)


threading.Thread(target=gossip, daemon=True).start()


@app.post("/sync")
def sync(data: dict):

    incoming_avg = data.get("avg_eta", 0)
    incoming_samples = data.get("samples", 1)

    total_samples = state["samples"] + incoming_samples

    if total_samples > 0:
        state["avg_eta"] = (
            (state["avg_eta"] * state["samples"]) +
            (incoming_avg * incoming_samples)
        ) / total_samples

        state["samples"] = total_samples

    logs.append(f"{region} ← Received avg {incoming_avg:.2f}")

    return {"status": "ok"}


@app.get("/logs")
def get_logs():
    return {"logs": logs[-10:]}