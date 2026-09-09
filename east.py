# ========================= east.py =========================

from fastapi import FastAPI, Response
import requests
import time
import threading
import os
import json
import psutil
import hashlib
from utils import (
    distance,
    estimate_time_from_distance,
    dynamic_traffic,
    get_rider_distance_from_option,
    get_prep_time,
    Observation,
    ObservationStore
)
import config
from config import get_region, get_gossip_peers

app = FastAPI(title="EdgeSync Regional Microservice - EAST")
region = "EAST"

# Global Volatile State, Sessions & Logs
obs_store = ObservationStore()
logs = []
start_time = time.time()
http_session = requests.Session()
blocked_peers = set()

# Structured Gossip Logging Setup
LOG_DIR = os.path.join("logs", "gossip")
os.makedirs(LOG_DIR, exist_ok=True)
gossip_log_file = os.path.join(LOG_DIR, f"gossip_{region.lower()}.jsonl")

def log_gossip_event(event_type, peer, payload_size, details):
    entry = {
        "timestamp": time.time(),
        "region": region,
        "event_type": event_type,
        "peer": peer,
        "payload_size_bytes": payload_size,
        "details": details
    }
    try:
        with open(gossip_log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass

# ---------------- HEALTH & OBSERVABILITY ----------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "region": region,
        "uptime_seconds": time.time() - start_time
    }

@app.get("/metrics")
def metrics():
    summary = obs_store.get_summary()
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return {
        "region": region,
        "avg_eta": summary["avg_eta"],
        "samples": summary["samples"],
        "stored_observations": len(obs_store.observations),
        "cpu_percent": process.cpu_percent(interval=None),
        "memory_rss_mb": memory_info.rss / (1024 * 1024),
        "thread_count": process.num_threads()
    }

@app.get("/state")
def get_state():
    sorted_ids = sorted(obs_store.observations.keys())
    state_hash = hashlib.sha256(json.dumps(sorted_ids).encode("utf-8")).hexdigest()
    return {
        "region": region,
        "observation_count": len(obs_store.observations),
        "state_hash": state_hash,
        "observation_ids": sorted_ids
    }

@app.post("/partition")
def set_partition(data: dict):
    peer = data.get("blocked_peer")
    if peer:
        blocked_peers.add(peer)
    return {"status": "partition_active", "blocked_peers": list(blocked_peers)}

@app.post("/unpartition")
def clear_partition(data: dict = None):
    peer = data.get("blocked_peer") if data else None
    if peer and peer in blocked_peers:
        blocked_peers.remove(peer)
    else:
        blocked_peers.clear()
    return {"status": "unpartitioned", "blocked_peers": list(blocked_peers)}

# ---------------- CUSTOM ETA ----------------
@app.post("/custom_eta")
def custom_eta(data: dict):
    t_start = time.perf_counter()
    source = data["source"]
    dest = data["destination"]
    food = data["food"]
    rider_option = data["rider"]

    # Feature Toggles Overrides
    partitioning_on = data.get("partitioning_enabled", config.REGIONAL_PARTITIONING)
    delegation_on = data.get("delegation_enabled", config.DELEGATION_ENABLED)
    dynamic_speed_on = data.get("dynamic_speed_enabled", config.DYNAMIC_SPEED_ENABLED)
    noise_on = data.get("prep_noise_enabled", True)

    if partitioning_on:
        dest_region = get_region(dest[0], dest[1]) if isinstance(dest, (list, tuple)) else get_region(dest)
    else:
        dest_region = region

    # Rider Pickup
    pickup = get_rider_distance_from_option(rider_option)

    # Food Prep
    if noise_on and not data.get("benchmark_mode", False):
        prep = get_prep_time(food)
    else:
        prep = 15.0 if food.lower() == "pizza" else (10.0 if food.lower() == "burger" else 7.0)

    # Dynamic Traffic
    traffic_level = data.get("traffic")
    if not traffic_level:
        traffic_level = dynamic_traffic() if dynamic_speed_on else "Medium"

    # Distributed Delivery
    net_ms = 0.0
    fallback_used = False
    if dest_region == region or not delegation_on:
        delivery = estimate_time_from_distance(
            distance(source, dest),
            traffic_level if dynamic_speed_on else "Medium"
        )
    else:
        target_url = f"{config.NODE_URLS.get(dest_region, config.NODE_URLS[region])}/calc_delivery"
        t_net_start = time.perf_counter()
        
        # Inter-service communication path network emulation & partition check
        net_delay_ms = float(data.get("network_delay_ms", 0.0))
        loss_rate = float(data.get("packet_loss_rate", 0.0))

        try:
            if dest_region in blocked_peers:
                raise requests.exceptions.ConnectionError(f"Network partition active between {region} and {dest_region}")

            if net_delay_ms > 0 or loss_rate > 0:
                try:
                    from experiments.network.network_emulator import global_emulator
                    global_emulator.inject_custom_delay(net_delay_ms, loss_rate=loss_rate)
                except Exception as net_err:
                    raise net_err

            res = http_session.post(target_url, json={
                "source": source,
                "dest": dest,
                "traffic": traffic_level if dynamic_speed_on else "Medium"
            }, timeout=config.GOSSIP_TIMEOUT).json()
            delivery = res["delivery_time"]
            fallback_used = False
        except Exception as e:
            # Fallback local delivery calculation on peer network failure
            delivery = estimate_time_from_distance(
                distance(source, dest),
                traffic_level if dynamic_speed_on else "Medium"
            )
            fallback_used = True
        net_ms = (time.perf_counter() - t_net_start) * 1000.0

    ETA = max(pickup, prep) + delivery

    # Create & Record Unique Observation if gossip/store enabled
    if config.GOSSIP_ENABLED:
        obs = Observation(origin_region=region, eta=ETA)
        obs_store.add_observation(obs.to_dict())
        obs_id = obs.obs_id
    else:
        obs_id = "no-gossip"

    t_end = time.perf_counter()
    t_total_ms = (t_end - t_start) * 1000.0
    t_sys_ms = max(0.001, t_total_ms - net_ms)

    return {
        "obs_id": obs_id,
        "ETA": ETA,
        "pickup": pickup,
        "prep": prep,
        "delivery": delivery,
        "traffic": traffic_level,
        "source_region": region,
        "dest_region": dest_region,
        "fallback_triggered": fallback_used,
        "latency_ms": {
            "total": round(t_total_ms, 3),
            "system": round(t_sys_ms, 3),
            "network": round(net_ms, 3),
            "computation": round(t_sys_ms, 3)
        }
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

# ---------------- GOSSIP PROTOCOL DAEMON ----------------
def gossip():
    while True:
        if config.GOSSIP_ENABLED:
            peers = get_gossip_peers(region)
            serializable_obs = obs_store.get_serializable_observations(limit=100)
            payload = {
                "sender": region,
                "observations": serializable_obs,
                "summary": obs_store.get_summary()
            }
            payload_bytes = len(json.dumps(payload))

            for peer in peers:
                peer_reg = [k for k, v in config.NODE_URLS.items() if v == peer]
                if peer_reg and peer_reg[0] in blocked_peers:
                    logs.append(f"{region} → Gossip blocked to {peer} (partition active)")
                    continue
                try:
                    sync_url = f"{peer}/sync"
                    res = http_session.post(sync_url, json=payload, timeout=config.GOSSIP_TIMEOUT)
                    if res.status_code == 200:
                        log_msg = f"{region} → Sent {len(serializable_obs)} obs to {peer}"
                        logs.append(log_msg)
                        log_gossip_event("SEND", peer, payload_bytes, {"sent_observations": len(serializable_obs)})
                    else:
                        logs.append(f"{region} → Gossip failed to {peer} (HTTP {res.status_code})")
                except Exception as e:
                    logs.append(f"{region} → Gossip failed to {peer}")
                    log_gossip_event("FAIL", peer, payload_bytes, {"error": str(e)})

        time.sleep(config.GOSSIP_INTERVAL)

threading.Thread(target=gossip, daemon=True).start()

# ---------------- GOSSIP SYNC ENDPOINT ----------------
@app.post("/sync")
def sync(data: dict):
    incoming_obs = data.get("observations", [])
    sender = data.get("sender", "UNKNOWN")

    added_count = obs_store.merge_observations(incoming_obs)

    summary = obs_store.get_summary()
    log_msg = f"{region} ← Received {len(incoming_obs)} obs from {sender} ({added_count} new)"
    logs.append(log_msg)
    log_gossip_event("RECEIVE", sender, len(json.dumps(data)), {
        "received_obs": len(incoming_obs),
        "new_added": added_count,
        "new_avg_eta": summary["avg_eta"],
        "total_samples": summary["samples"]
    })

    return {
        "status": "ok",
        "added": added_count,
        "total_samples": summary["samples"],
        "avg_eta": summary["avg_eta"]
    }

@app.get("/logs")
def get_logs():
    return {"logs": logs[-10:]}