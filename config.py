import os

# Geographic bounds for Mumbai Delivery Zones
# EAST: lat >= 19.05, lon >= 72.85 (e.g. Powai, Kanjurmarg)
# WEST: lat >= 19.05, lon < 72.85  (e.g. Bandra, Juhu)
# CENTRAL: lat < 19.05             (e.g. Dadar, South Mumbai)

def get_region(lat, lon=None):
    if lon is None and isinstance(lat, (list, tuple)):
        lat, lon = lat[0], lat[1]
    if lat < 19.05:
        return "CENTRAL"
    elif lon < 72.85:
        return "WEST"
    else:
        return "EAST"

# -------- EXPERIMENTAL FEATURE TOGGLES & SETTINGS --------
MODE = os.getenv("EDGESYNC_MODE", "edgesync")
REGIONAL_PARTITIONING = os.getenv("EDGESYNC_PARTITIONING_ENABLED", "true").lower() == "true"
DELEGATION_ENABLED = os.getenv("EDGESYNC_DELEGATION_ENABLED", "true").lower() == "true"
GOSSIP_ENABLED = os.getenv("EDGESYNC_GOSSIP_ENABLED", "true").lower() == "true"
DYNAMIC_SPEED_ENABLED = os.getenv("EDGESYNC_DYNAMIC_SPEED_ENABLED", "true").lower() == "true"

BENCHMARK_MODE = os.getenv("EDGESYNC_BENCHMARK_MODE", "false").lower() == "true"
DOMAIN_DELAY = os.getenv("EDGESYNC_DOMAIN_DELAY", "true").lower() == "true"

GOSSIP_INTERVAL = float(os.getenv("EDGESYNC_GOSSIP_INTERVAL", "5.0"))
GOSSIP_TOPOLOGY = os.getenv("EDGESYNC_GOSSIP_TOPOLOGY", "ring").lower() # ring, fully_connected, peer_list
GOSSIP_TIMEOUT = float(os.getenv("EDGESYNC_GOSSIP_TIMEOUT", "10.0"))
GOSSIP_RETRIES = int(os.getenv("EDGESYNC_GOSSIP_RETRIES", "1"))

RANDOM_SEED = int(os.getenv("EDGESYNC_SEED", "42"))
MAX_OBSERVATIONS_STORED = int(os.getenv("EDGESYNC_MAX_STORED_OBS", "500"))
OBSERVATION_WINDOW_SECONDS = int(os.getenv("EDGESYNC_OBS_WINDOW", "3600"))

# Dynamic peer mapping based on host
NODE_HOST = os.getenv("EDGESYNC_NODE_HOST", "127.0.0.1")
NODE_URLS = {
    "EAST": f"http://{NODE_HOST}:8000",
    "WEST": f"http://{NODE_HOST}:9000",
    "CENTRAL": f"http://{NODE_HOST}:10000"
}

def get_gossip_peers(current_region):
    if GOSSIP_TOPOLOGY == "fully_connected":
        return [url for r, url in NODE_URLS.items() if r != current_region]
    elif GOSSIP_TOPOLOGY == "peer_list":
        # Static peer list
        return [url for r, url in NODE_URLS.items() if r != current_region]
    else:
        # Default Ring Topology: EAST -> WEST -> CENTRAL -> EAST
        ring_next = {
            "EAST": f"http://{NODE_HOST}:9000",
            "WEST": f"http://{NODE_HOST}:10000",
            "CENTRAL": f"http://{NODE_HOST}:8000"
        }
        return [ring_next.get(current_region)]