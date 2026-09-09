import math
import random
import uuid
import time
from datetime import datetime
import config

# -------- SEEDING SETUP --------
if config.RANDOM_SEED >= 0:
    random.seed(config.RANDOM_SEED)

def set_deterministic_seed(seed=42):
    random.seed(seed)

# -------- OBSERVATION MODEL & RESERVOIR STORE --------
class Observation:
    def __init__(self, obs_id=None, timestamp=None, origin_region="EAST", eta=0.0):
        self.obs_id = obs_id or str(uuid.uuid4())
        self.timestamp = timestamp or time.time()
        self.origin_region = origin_region
        self.eta = eta

    def to_dict(self):
        return {
            "obs_id": self.obs_id,
            "timestamp": self.timestamp,
            "origin_region": self.origin_region,
            "eta": self.eta
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            obs_id=data.get("obs_id"),
            timestamp=data.get("timestamp"),
            origin_region=data.get("origin_region"),
            eta=data.get("eta", 0.0)
        )


class ObservationStore:
    def __init__(self, max_capacity=config.MAX_OBSERVATIONS_STORED, window_seconds=config.OBSERVATION_WINDOW_SECONDS):
        self.max_capacity = max_capacity
        self.window_seconds = window_seconds
        # Key: obs_id (str) -> dict
        self.observations = {}

    def add_observation(self, obs_dict):
        obs_id = obs_dict.get("obs_id")
        if not obs_id:
            obs_id = str(uuid.uuid4())
            obs_dict["obs_id"] = obs_id
        if "timestamp" not in obs_dict:
            obs_dict["timestamp"] = time.time()

        self.observations[obs_id] = obs_dict
        self._prune()

    def merge_observations(self, incoming_obs_list):
        new_added = 0
        for obs in incoming_obs_list:
            obs_id = obs.get("obs_id")
            if obs_id and obs_id not in self.observations:
                self.observations[obs_id] = obs
                new_added += 1
        self._prune()
        return new_added

    def _prune(self):
        now = time.time()
        # Remove expired items outside window if window specified
        if self.window_seconds > 0:
            expired_keys = [
                k for k, v in self.observations.items() 
                if (now - v.get("timestamp", now)) > self.window_seconds
            ]
            for k in expired_keys:
                del self.observations[k]

        # Enforce max capacity by removing oldest observations
        if len(self.observations) > self.max_capacity:
            sorted_obs = sorted(self.observations.items(), key=lambda item: item[1].get("timestamp", 0))
            excess = len(self.observations) - self.max_capacity
            for k, _ in sorted_obs[:excess]:
                del self.observations[k]

    def get_summary(self):
        if not self.observations:
            return {"avg_eta": 0.0, "samples": 0}
        total_eta = sum(obs.get("eta", 0.0) for obs in self.observations.values())
        count = len(self.observations)
        return {
            "avg_eta": total_eta / count,
            "samples": count
        }

    def get_serializable_observations(self, limit=100):
        # Return most recent observations for gossip transfer
        sorted_obs = sorted(self.observations.values(), key=lambda x: x.get("timestamp", 0), reverse=True)
        return sorted_obs[:limit]


# -------- DISTANCE (HAVERSINE) --------
def distance(p1, p2):
    R = 6371
    lat1, lon1 = math.radians(p1[0]), math.radians(p1[1])
    lat2, lon2 = math.radians(p2[0]), math.radians(p2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# -------- SPEED MODEL --------
def estimate_time_from_distance(distance_km, traffic_level):
    speed_map = {
        "Low": 35,
        "Medium": 25,
        "High": 15
    }

    speed = speed_map.get(traffic_level, 25)
    return (distance_km / speed) * 60

# -------- DYNAMIC TRAFFIC --------
def dynamic_traffic():
    hour = datetime.now().hour

    if 8 <= hour <= 11 or 17 <= hour <= 21:
        return "High"
    elif 12 <= hour <= 16:
        return "Medium"
    else:
        return "Low"

# -------- RIDER DISTANCE --------
def get_rider_distance_from_option(option):
    ranges = {
        "Near (0.5-2 km)": (0.5, 2),
        "Medium (2-5 km)": (2, 5),
        "Far (5-8 km)": (5, 8)
    }

    low, high = ranges.get(option, (2, 5))
    return ((low + high) / 2) * random.uniform(0.9, 1.1)

# -------- FOOD PREP (BUG FIXED WITH LOWERCASE NORMALIZATION) --------
def get_prep_time(food):
    prep_times = {
        "pizza": (12, 18),
        "burger": (8, 12),
        "sandwich": (5, 8),
        "taco": (6, 10)
    }

    # Normalize food string to lowercase to fix case-sensitivity bug
    food_key = str(food).strip().lower()
    low, high = prep_times.get(food_key, (5, 10))
    return ((low + high) / 2) * random.uniform(0.9, 1.1)
