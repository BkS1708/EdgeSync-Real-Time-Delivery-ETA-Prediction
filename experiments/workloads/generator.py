import sys
import os
import random
import json
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils import set_deterministic_seed

FOOD_TYPES = ["pizza", "burger", "sandwich", "taco"]
RIDER_OPTIONS = ["Near (0.5-2 km)", "Medium (2-5 km)", "Far (5-8 km)"]
TRAFFIC_LEVELS = ["Low", "Medium", "High"]

LAT_MIN, LAT_MAX = 18.90, 19.25
LON_MIN, LON_MAX = 72.80, 72.98

class WorkloadGenerator:
    def __init__(self, seed=42):
        self.seed = seed
        set_deterministic_seed(seed)

    def _determine_region(self, lat, lon):
        if lat < 19.05:
            return "CENTRAL"
        elif lon < 72.85:
            return "WEST"
        else:
            return "EAST"

    def generate_workload(self, count=1000, pattern="uniform", locality_ratio=None):
        set_deterministic_seed(self.seed)
        workload = []

        for i in range(count):
            req_id = f"req_{i+1:04d}"

            if pattern == "east_heavy":
                src_lat = random.uniform(19.06, 19.20)
                src_lon = random.uniform(72.86, 72.95)
            elif pattern == "west_heavy":
                src_lat = random.uniform(19.06, 19.20)
                src_lon = random.uniform(72.80, 72.84)
            elif pattern == "central_heavy":
                src_lat = random.uniform(18.90, 19.04)
                src_lon = random.uniform(72.80, 72.95)
            else: # Uniform
                src_lat = random.uniform(LAT_MIN, LAT_MAX)
                src_lon = random.uniform(LON_MIN, LON_MAX)

            src_region = self._determine_region(src_lat, src_lon)

            if locality_ratio is not None:
                if random.random() < locality_ratio:
                    if src_region == "CENTRAL":
                        dst_lat = random.uniform(18.90, 19.04)
                        dst_lon = random.uniform(72.80, 72.95)
                    elif src_region == "WEST":
                        dst_lat = random.uniform(19.06, 19.20)
                        dst_lon = random.uniform(72.80, 72.84)
                    else: # EAST
                        dst_lat = random.uniform(19.06, 19.20)
                        dst_lon = random.uniform(72.86, 72.95)
                else:
                    dst_lat = random.uniform(LAT_MIN, LAT_MAX)
                    dst_lon = random.uniform(LON_MIN, LON_MAX)
            else:
                dst_lat = random.uniform(LAT_MIN, LAT_MAX)
                dst_lon = random.uniform(LON_MIN, LON_MAX)

            dst_region = self._determine_region(dst_lat, dst_lon)

            food = random.choice(FOOD_TYPES)
            rider = random.choice(RIDER_OPTIONS)
            traffic = random.choice(TRAFFIC_LEVELS)

            workload.append({
                "request_id": req_id,
                "source": [round(src_lat, 6), round(src_lon, 6)],
                "destination": [round(dst_lat, 6), round(dst_lon, 6)],
                "food": food,
                "rider": rider,
                "traffic": traffic,
                "random_seed": self.seed,
                "source_region": src_region,
                "dest_region": dst_region,
                "is_cross_region": (src_region != dst_region),
                "pattern": pattern
            })

        return workload

    def save_benchmark_workload(self, filepath="experiments/workloads/benchmark_workload.json", count=1000):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        workload = self.generate_workload(count=count, pattern="uniform")
        with open(filepath, "w") as f:
            json.dump(workload, f, indent=2)

        sha256_hash = self.get_workload_hash(filepath)
        print(f"Generated Benchmark Workload ({count} requests) -> {filepath}")
        print(f"SHA-256 Workload Hash: {sha256_hash}")
        return filepath, sha256_hash

    @staticmethod
    def get_workload_hash(filepath="experiments/workloads/benchmark_workload.json"):
        if not os.path.exists(filepath):
            return None
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()

if __name__ == "__main__":
    gen = WorkloadGenerator(seed=42)
    gen.save_benchmark_workload()
