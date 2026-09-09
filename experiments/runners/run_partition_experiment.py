import time
import os
import requests
import json
import csv
from experiments.config.experiment_config import ExperimentConfig
from experiments.workloads.generator import WorkloadGenerator
from experiments.analysis.statistics import calculate_stats, generate_markdown_table
from experiments.plots.plotter import plot_partition_locality

def run_partition_experiment(config=None):
    if not config:
        config = ExperimentConfig(name="partitioning")

    results_dir = os.path.join("results", "phase3", "partitioning")
    os.makedirs(results_dir, exist_ok=True)

    print("=== Executing Geographic Locality, Hotspot & Partitioning Suite ===")

    generator = WorkloadGenerator(seed=config.random_seed)

    # 1. Spatial Locality Sweep (90% to 10% intra-region)
    locality_ratios = [0.90, 0.70, 0.50, 0.30, 0.10]
    cross_rates = []
    mean_lats = []
    raw_locality_records = []

    print("\n--- Phase A: Spatial Locality Ratio Sweep (90% down to 10%) ---")
    for loc in locality_ratios:
        workload = generator.generate_workload(count=100, pattern="uniform", locality_ratio=loc)
        cross_count = sum(1 for req in workload if req["is_cross_region"])
        cross_pct = (cross_count / len(workload)) * 100.0

        latencies = []
        sys_latencies = []
        for req in workload:
            t0 = time.perf_counter()
            try:
                res = requests.post("http://localhost:8000/custom_eta", json={
                    "source": req["source"], "destination": req["destination"],
                    "food": req["food"], "rider": req["rider"], "traffic": req["traffic"]
                }, timeout=5.0).json()
                t_tot = (time.perf_counter() - t0) * 1000.0
                t_sys = res.get("latency_ms", {}).get("system", t_tot)
                t_net = res.get("latency_ms", {}).get("network", 0.0)
                success = True
            except Exception:
                t_tot = (time.perf_counter() - t0) * 1000.0
                t_sys = t_tot
                t_net = 0.0
                success = False

            latencies.append(t_tot)
            sys_latencies.append(t_sys)

            raw_locality_records.append({
                "locality_ratio": loc,
                "locality_pct": int(loc * 100),
                "request_id": req["request_id"],
                "source_region": req["source_region"],
                "dest_region": req["dest_region"],
                "is_cross_region": req["is_cross_region"],
                "total_latency_ms": round(t_tot, 3),
                "system_latency_ms": round(t_sys, 3),
                "network_latency_ms": round(t_net, 3),
                "success": success
            })

        stats = calculate_stats(latencies)
        cross_rates.append(round(cross_pct, 1))
        mean_lats.append(stats["mean"])
        print(f"  Locality {int(loc*100)}% Intra -> Cross-Region Rate={cross_pct:4.1f}%, Mean Latency={stats['mean']:5.2f}ms, P95={stats['p95']:5.2f}ms")

    # Save raw locality CSV
    raw_loc_csv = os.path.join(results_dir, "partition_raw_locality.csv")
    with open(raw_loc_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["locality_ratio", "locality_pct", "request_id", "source_region", "dest_region", "is_cross_region", "total_latency_ms", "system_latency_ms", "network_latency_ms", "success"])
        writer.writeheader()
        writer.writerows(raw_locality_records)

    plot_partition_locality([int(l*100) for l in locality_ratios], cross_rates, mean_lats, os.path.join(results_dir, "partition_locality.png"))

    # 2. Hotspot Workload & Load Imbalance
    patterns = ["uniform", "east_heavy", "west_heavy", "central_heavy"]
    headers_hotspot = ["Traffic Pattern", "EAST Reqs", "WEST Reqs", "CENTRAL Reqs", "Load Imbalance Ratio", "Mean Latency (ms)", "P95 Latency (ms)"]
    rows_hotspot = []
    raw_hotspot_records = []

    print("\n--- Phase B: Hotspot Load Distribution & Node Imbalance ---")
    for pat in patterns:
        workload = generator.generate_workload(count=300, pattern=pat)
        east_c = sum(1 for r in workload if r["source_region"] == "EAST")
        west_c = sum(1 for r in workload if r["source_region"] == "WEST")
        central_c = sum(1 for r in workload if r["source_region"] == "CENTRAL")
        
        max_c = max(east_c, west_c, central_c)
        min_c = max(1, min(east_c, west_c, central_c))
        imbalance = round(max_c / min_c, 2)

        latencies = []
        for req in workload[:100]:
            t0 = time.perf_counter()
            try:
                res = requests.post("http://localhost:8000/custom_eta", json={
                    "source": req["source"], "destination": req["destination"],
                    "food": req["food"], "rider": req["rider"], "traffic": req["traffic"]
                }, timeout=5.0).json()
                t_tot = (time.perf_counter() - t0) * 1000.0
                success = True
            except Exception:
                t_tot = (time.perf_counter() - t0) * 1000.0
                success = False

            latencies.append(t_tot)
            raw_hotspot_records.append({
                "pattern": pat,
                "request_id": req["request_id"],
                "source_region": req["source_region"],
                "dest_region": req["dest_region"],
                "latency_ms": round(t_tot, 3),
                "success": success
            })

        stats = calculate_stats(latencies)
        rows_hotspot.append([pat.upper(), east_c, west_c, central_c, f"{imbalance}x", stats["mean"], stats["p95"]])
        print(f"  Pattern {pat:14s}: EAST={east_c:3d}, WEST={west_c:3d}, CENTRAL={central_c:3d} (Imbalance={imbalance:4.2f}x, Mean Lat={stats['mean']}ms)")

    # Save raw hotspot CSV
    raw_hot_csv = os.path.join(results_dir, "partition_raw_hotspots.csv")
    with open(raw_hot_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["pattern", "request_id", "source_region", "dest_region", "latency_ms", "success"])
        writer.writeheader()
        writer.writerows(raw_hotspot_records)

    md_table = generate_markdown_table(headers_hotspot, rows_hotspot)

    summary = {
        "locality_sweep": {
            "locality_pct": [int(l*100) for l in locality_ratios],
            "cross_region_rate_pct": cross_rates,
            "mean_latency_ms": mean_lats
        },
        "hotspot_distribution": [
            {"pattern": r[0], "east_count": r[1], "west_count": r[2], "central_count": r[3], "imbalance_ratio": r[4], "mean_lat_ms": r[5], "p95_lat_ms": r[6]}
            for r in rows_hotspot
        ]
    }

    with open(os.path.join(results_dir, "partitioning_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    with open(os.path.join(results_dir, "partitioning_summary.md"), "w") as f:
        f.write("# Geographic Partitioning & Hotspot Distribution Summary\n\n" + md_table + "\n")

    print("\n--- Hotspot Distribution Summary Table ---")
    print(md_table)
    return summary

if __name__ == "__main__":
    run_partition_experiment()
