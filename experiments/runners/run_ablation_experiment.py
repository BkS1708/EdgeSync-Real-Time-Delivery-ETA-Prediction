import time
import os
import requests
import json
import csv
from experiments.config.experiment_config import ExperimentConfig
from experiments.workloads.generator import WorkloadGenerator
from experiments.analysis.statistics import calculate_stats, generate_markdown_table
from experiments.plots.plotter import plot_ablation_comparison

def run_ablation_experiment(config=None, count=200):
    if not config:
        config = ExperimentConfig(name="ablation")

    results_dir = os.path.join("results", "phase3", "ablation")
    os.makedirs(results_dir, exist_ok=True)

    print("=== Executing Component Ablation Suite (Pure System & Total Latencies) ===")
    
    workload_path = "experiments/workloads/benchmark_workload.json"
    if not os.path.exists(workload_path):
        gen = WorkloadGenerator(seed=config.random_seed)
        gen.save_benchmark_workload(filepath=workload_path, count=1000)

    with open(workload_path, "r") as f:
        workload = json.load(f)[:count]

    ablation_variants = [
        ("Full EdgeSync Platform", {"partitioning_enabled": True, "delegation_enabled": True, "gossip_enabled": True, "dynamic_speed_enabled": True, "prep_noise_enabled": True}),
        ("Ablation 1: Partitioning OFF (Single Node)", {"partitioning_enabled": False, "delegation_enabled": True, "gossip_enabled": True, "dynamic_speed_enabled": True, "prep_noise_enabled": True}),
        ("Ablation 2: Cross-Delegation OFF (Local Math)", {"partitioning_enabled": True, "delegation_enabled": False, "gossip_enabled": True, "dynamic_speed_enabled": True, "prep_noise_enabled": True}),
        ("Ablation 3: Gossip Synchronization Disabled", {"partitioning_enabled": True, "delegation_enabled": True, "gossip_enabled": False, "dynamic_speed_enabled": True, "prep_noise_enabled": True}),
        ("Ablation 4: Dynamic Traffic Model Disabled", {"partitioning_enabled": True, "delegation_enabled": True, "gossip_enabled": True, "dynamic_speed_enabled": False, "prep_noise_enabled": True}),
        ("Ablation 5: Prep Noise Disabled", {"partitioning_enabled": True, "delegation_enabled": True, "gossip_enabled": True, "dynamic_speed_enabled": True, "prep_noise_enabled": False})
    ]

    labels = []
    p95_values = []
    mean_values = []
    summary_data = {}
    raw_ablation_records = []

    for name, payload_toggles in ablation_variants:
        print(f"Benchmarking Variant: {name} ({len(workload)} requests)...")
        sys_latencies = []
        tot_latencies = []
        
        for req in workload:
            payload = {
                "source": req["source"],
                "destination": req["destination"],
                "food": req["food"],
                "rider": req["rider"],
                "traffic": req["traffic"]
            }
            payload.update(payload_toggles)

            t0 = time.perf_counter()
            try:
                res = requests.post("http://localhost:8000/custom_eta", json=payload, timeout=5.0).json()
                t_total_ms = (time.perf_counter() - t0) * 1000.0
                t_sys_ms = res.get("latency_ms", {}).get("system", t_total_ms)
                t_net_ms = res.get("latency_ms", {}).get("network", 0.0)
                eta_val = res.get("ETA", 0.0)
                success = True
            except Exception:
                t_total_ms = (time.perf_counter() - t0) * 1000.0
                t_sys_ms = t_total_ms
                t_net_ms = 0.0
                eta_val = 0.0
                success = False

            sys_latencies.append(t_sys_ms)
            tot_latencies.append(t_total_ms)

            raw_ablation_records.append({
                "variant": name,
                "request_id": req["request_id"],
                "total_latency_ms": round(t_total_ms, 3),
                "system_latency_ms": round(t_sys_ms, 3),
                "network_latency_ms": round(t_net_ms, 3),
                "eta_minutes": round(eta_val, 2),
                "success": success
            })

        stats_sys = calculate_stats(sys_latencies)
        stats_tot = calculate_stats(tot_latencies)

        labels.append(name)
        p95_values.append(stats_sys["p95"])
        mean_values.append(stats_sys["mean"])
        
        summary_data[name] = {
            "system_stats": stats_sys,
            "total_stats": stats_tot
        }
        print(f"  {name}: System Mean={stats_sys['mean']:5.2f}ms, Total Mean={stats_tot['mean']:5.2f}ms, System P95={stats_sys['p95']:5.2f}ms")

    # 1. Save Raw CSV
    raw_csv_path = os.path.join(results_dir, "ablation_raw_results.csv")
    with open(raw_csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["variant", "request_id", "total_latency_ms", "system_latency_ms", "network_latency_ms", "eta_minutes", "success"])
        writer.writeheader()
        writer.writerows(raw_ablation_records)

    # 2. Generate Plot & Tables
    plot_path = os.path.join(results_dir, "ablation_comparison.png")
    plot_ablation_comparison(labels, p95_values, plot_path)

    headers = ["Ablation Variant", "Count", "System Mean (ms)", "Total Mean (ms)", "P50 (ms)", "P90 (ms)", "P95 (ms)", "P99 (ms)", "StdDev"]
    rows = []
    for lbl in labels:
        st_sys = summary_data[lbl]["system_stats"]
        st_tot = summary_data[lbl]["total_stats"]
        rows.append([lbl, st_sys["count"], st_sys["mean"], st_tot["mean"], st_sys["p50"], st_sys["p90"], st_sys["p95"], st_sys["p99"], st_sys["stddev"]])

    # Write ablation_summary.csv
    csv_path = os.path.join(results_dir, "ablation_summary.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    md_table = generate_markdown_table(headers, rows)

    with open(os.path.join(results_dir, "ablation_summary.md"), "w") as f:
        f.write("# Component Ablation Study Summary\n\n" + md_table + "\n")

    with open(os.path.join(results_dir, "ablation_summary.json"), "w") as f:
        json.dump(summary_data, f, indent=2)

    print("\n--- Ablation Study Summary Table ---")
    print(md_table)
    return summary_data

if __name__ == "__main__":
    run_ablation_experiment()
