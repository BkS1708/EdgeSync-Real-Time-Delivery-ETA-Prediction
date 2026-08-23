import math
import random
from datetime import datetime

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

    speed = speed_map[traffic_level]
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

    low, high = ranges[option]
    return ((low + high) / 2) * random.uniform(0.9, 1.1)

# -------- FOOD PREP --------
def get_prep_time(food):
    prep_times = {
        "pizza": (12, 18),
        "burger": (8, 12),
        "sandwich": (5, 8),
        "taco": (6, 10)
    }

    low, high = prep_times.get(food, (5, 10))
    return ((low + high) / 2) * random.uniform(0.9, 1.1)
