import time
import os
import csv
import json

class MetricsCollector:
    def __init__(self, experiment_name="experiment", output_dir="results"):
        self.experiment_name = experiment_name
        self.output_dir = os.path.join(output_dir, experiment_name)
        os.makedirs(self.output_dir, exist_ok=True)
        self.records = []

    def record_request(self, req_id, src_region, dst_region, traffic, dist_km, eta,
                       pickup, prep, delivery, total_lat_ms, comp_lat_ms, net_lat_ms,
                       success=True, error_msg="", mode="edgesync", gossip_enabled=True,
                       gossip_interval=5.0, node_count=3):
        
        cross_region = (src_region != dst_region)
        record = {
            "request_id": req_id,
            "timestamp": time.time(),
            "mode": mode,
            "source_region": src_region,
            "dest_region": dst_region,
            "cross_region": cross_region,
            "traffic": traffic,
            "distance_km": round(dist_km, 4),
            "eta": round(eta, 2),
            "pickup_time": round(pickup, 2),
            "prep_time": round(prep, 2),
            "delivery_time": round(delivery, 2),
            "request_latency_ms": round(total_lat_ms, 3),
            "computation_latency_ms": round(comp_lat_ms, 3),
            "network_latency_ms": round(net_lat_ms, 3),
            "success": success,
            "error": error_msg,
            "gossip_enabled": gossip_enabled,
            "gossip_interval": gossip_interval,
            "node_count": node_count
        }
        self.records.append(record)

    def save_to_csv(self, filename="raw_results.csv"):
        if not self.records:
            return
        filepath = os.path.join(self.output_dir, filename)
        fieldnames = list(self.records[0].keys())
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.records)

    def save_to_json(self, filename="raw_results.json"):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(self.records, f, indent=2)

    def clear(self):
        self.records = []
