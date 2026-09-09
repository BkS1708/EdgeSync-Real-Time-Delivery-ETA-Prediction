import time
import os
import requests
import json
import random
import csv
import pandas as pd
from experiments.config.experiment_config import ExperimentConfig
from experiments.workloads.generator import WorkloadGenerator
from experiments.metrics.collector import MetricsCollector
from experiments.analysis.statistics import calculate_stats, calculate_paired_ttest, generate_markdown_table
from experiments.plots.plotter import plot_latency_cdf, plot_latency_breakdown
from utils import distance

def run_latency_experiment(config=None, num_requests=1000, warmup_count=50):
    if not config:
        config = ExperimentConfig(name="latency")

    results_dir = os.path.join("results", "phase3", "latency")
    os.makedirs(results_dir, exist_ok=True)
    collector = MetricsCollector(experiment_name="latency", output_dir=os.path.join("results", "phase3"))

    # 1. Load Single Hashable Benchmark Workload
    workload_path = "experiments/workloads/benchmark_workload.json"
    if not os.path.exists(workload_path):
        gen = WorkloadGenerator(seed=config.random_seed)
        gen.save_benchmark_workload(filepath=workload_path, count=num_requests)

    with open(workload_path, "r") as f:
        full_workload_file = json.load(f)
        workload = full_workload_file[:num_requests]

    workload_hash = WorkloadGenerator.get_workload_hash(workload_path)
    print(f"=== Executing Matched Latency Experiment ({len(workload)} requests) ===")
    print(f"Workload Hash: {workload_hash}")

    node_urls = {
        "EAST": "http://localhost:8000",
        "WEST": "http://localhost:9000",
        "CENTRAL": "http://localhost:10000"
    }

    # Architectures to benchmark
    architectures = [
        "Full EdgeSync Cluster",
        "Intra-Region EdgeSync",
        "Cross-Region EdgeSync",
        "EdgeSync w/o Gossip",
        "EdgeSync w/o Partitioning",
        "Centralized Baseline"
    ]

    # Balanced / Randomized execution order to avoid OS/thermal/cache bias
    random.seed(config.random_seed)
    random.shuffle(architectures)
    print(f"Randomized Trial Order: {' -> '.join(architectures)}")

    results_by_arch = {arch: {"total": [], "system": [], "network": [], "req_ids": []} for arch in architectures}

    # Generate separate warmup requests outside measured workload
    gen = WorkloadGenerator(seed=9999)
    warmup_workload = gen.generate_workload(count=warmup_count, pattern="uniform")

    # 2. Benchmark Loop
    for arch in architectures:
        print(f"\nBenchmarking Architecture: {arch}...")
        
        # Warm-up phase (outside measured N)
        print(f"  Executing {warmup_count} warm-up requests (discarded)...")
        for req in warmup_workload:
            try:
                requests.post("http://localhost:8000/custom_eta", json={
                    "source": req["source"], "destination": req["destination"],
                    "food": req["food"], "rider": req["rider"], "traffic": req["traffic"]
                }, timeout=3.0)
            except Exception:
                pass

        # Measurement Phase
        print(f"  Measuring steady-state requests for {arch}...")
        for req in workload:
            src = req["source"]
            dst = req["destination"]
            src_reg = req["source_region"]
            dst_reg = req["dest_region"]

            # Filter for specific intra/cross subsets if requested
            if arch == "Intra-Region EdgeSync" and src_reg != dst_reg:
                continue
            if arch == "Cross-Region EdgeSync" and src_reg == dst_reg:
                continue

            if arch == "Centralized Baseline":
                target_url = "http://localhost:8000/custom_eta"
                payload = {
                    "source": src, "destination": dst, "food": req["food"],
                    "rider": req["rider"], "traffic": req["traffic"],
                    "partitioning_enabled": False, "delegation_enabled": False
                }
            elif arch == "EdgeSync w/o Partitioning":
                target_url = "http://localhost:8000/custom_eta"
                payload = {
                    "source": src, "destination": dst, "food": req["food"],
                    "rider": req["rider"], "traffic": req["traffic"],
                    "partitioning_enabled": False
                }
            elif arch == "EdgeSync w/o Gossip":
                target_url = f"{node_urls[src_reg]}/custom_eta"
                payload = {
                    "source": src, "destination": dst, "food": req["food"],
                    "rider": req["rider"], "traffic": req["traffic"],
                    "gossip_enabled": False
                }
            else: # Standard EdgeSync (Full, Intra, Cross)
                target_url = f"{node_urls[src_reg]}/custom_eta"
                payload = {
                    "source": src, "destination": dst, "food": req["food"],
                    "rider": req["rider"], "traffic": req["traffic"]
                }

            t0 = time.perf_counter()
            try:
                res = requests.post(target_url, json=payload, timeout=5.0).json()
                t_total_ms = (time.perf_counter() - t0) * 1000.0

                lat_info = res.get("latency_ms", {})
                t_sys_ms = lat_info.get("system", t_total_ms)
                t_net_ms = lat_info.get("network", 0.0)

                results_by_arch[arch]["total"].append(t_total_ms)
                results_by_arch[arch]["system"].append(t_sys_ms)
                results_by_arch[arch]["network"].append(t_net_ms)
                results_by_arch[arch]["req_ids"].append(req["request_id"])

                collector.record_request(
                    req_id=req["request_id"], src_region=src_reg, dst_region=dst_reg,
                    traffic=req["traffic"], dist_km=distance(src, dst),
                    eta=res.get("ETA", 0.0), pickup=res.get("pickup", 0.0), prep=res.get("prep", 0.0), delivery=res.get("delivery", 0.0),
                    total_lat_ms=t_total_ms, comp_lat_ms=t_sys_ms, net_lat_ms=t_net_ms,
                    success=True, mode=arch
                )

            except Exception as e:
                t_total_ms = (time.perf_counter() - t0) * 1000.0
                collector.record_request(
                    req_id=req["request_id"], src_region=src_reg, dst_region=dst_reg,
                    traffic=req["traffic"], dist_km=distance(src, dst),
                    eta=0.0, pickup=0.0, prep=0.0, delivery=0.0,
                    total_lat_ms=t_total_ms, comp_lat_ms=0.0, net_lat_ms=0.0,
                    success=False, error_msg=str(e), mode=arch
                )

    # 3. Compute Statistical Summaries & Strict Request ID Paired Significance
    stats_summary = {}
    total_cdf_data = {}
    breakdown_data = {"System Overhead": [], "Cross-Node Network": []}
    breakdown_cats = []

    # Map per-request latencies by req_id for strict pairing
    req_map = {arch: {} for arch in architectures}
    for arch, metrics in results_by_arch.items():
        for req_id, tot_lat in zip(metrics.get("req_ids", []), metrics["total"]):
            req_map[arch][req_id] = tot_lat

    central_map = req_map.get("Centralized Baseline", {})

    for arch in architectures:
        metrics = results_by_arch[arch]
        if metrics["total"]:
            stats_tot = calculate_stats(metrics["total"])
            stats_sys = calculate_stats(metrics["system"])
            stats_net = calculate_stats(metrics["network"])

            # Paired sample comparison by matching request_id
            common_ids = [rid for rid in metrics.get("req_ids", []) if rid in central_map]
            if common_ids and arch != "Centralized Baseline":
                arch_paired = [req_map[arch][rid] for rid in common_ids]
                cent_paired = [central_map[rid] for rid in common_ids]
                ttest = calculate_paired_ttest(arch_paired, cent_paired)
            else:
                ttest = {"t_stat": 0.0, "p_val": 1.0, "mean_diff": 0.0, "significant": False}

            stats_summary[arch] = {
                "sample_count": len(metrics["total"]),
                "total_stats": stats_tot,
                "system_stats": stats_sys,
                "network_stats": stats_net,
                "ttest_vs_centralized": ttest,
                "paired_sample_count": len(common_ids)
            }

            total_cdf_data[arch] = metrics["total"]
            breakdown_cats.append(arch)
            breakdown_data["System Overhead"].append(stats_sys["mean"])
            breakdown_data["Cross-Node Network"].append(stats_net["mean"])

    # 4. Save Figures & Reports
    cdf_path = os.path.join(results_dir, "latency_cdf.png")
    plot_latency_cdf(total_cdf_data, cdf_path)

    decomp_path = os.path.join(results_dir, "latency_decomposition.png")
    plot_latency_breakdown(breakdown_cats, breakdown_data, decomp_path)

    collector.save_to_csv("latency_raw_results.csv")
    collector.save_to_json("latency_raw_results.json")

    # Also save directly in results/phase3/latency/
    csv_raw_path = os.path.join(results_dir, "latency_raw_results.csv")
    with open(csv_raw_path, "w", newline="") as f:
        if collector.records:
            writer = csv.DictWriter(f, fieldnames=list(collector.records[0].keys()))
            writer.writeheader()
            writer.writerows(collector.records)

    json_raw_path = os.path.join(results_dir, "latency_raw_results.json")
    with open(json_raw_path, "w") as f:
        json.dump(collector.records, f, indent=2)

    # Generate Markdown Summary Table
    headers = ["Architecture", "Count", "Total Mean (ms)", "System Mean (ms)", "Net Mean (ms)", "P50 (ms)", "P95 (ms)", "P99 (ms)", "StdDev", "p-value vs Central"]
    rows = []
    for arch, data in stats_summary.items():
        st = data["total_stats"]
        sys_m = data["system_stats"]["mean"]
        net_m = data["network_stats"]["mean"]
        pval = data["ttest_vs_centralized"]["p_val"]
        rows.append([arch, st["count"], st["mean"], sys_m, net_m, st["p50"], st["p95"], st["p99"], st["stddev"], f"{pval:.6f}"])

    md_table = generate_markdown_table(headers, rows)

    with open(os.path.join(results_dir, "latency_summary.md"), "w") as f:
        f.write("# Matched Decision Latency Benchmark Summary\n\n")
        f.write(f"**Workload Hash:** `{workload_hash}`\n\n")
        f.write(md_table + "\n")

    with open(os.path.join(results_dir, "latency_summary.json"), "w") as f:
        json.dump(stats_summary, f, indent=2)

    print("\n--- Latency Experiment Summary ---")
    print(md_table)
    print(f"\nCDF Plot saved: {cdf_path}")
    print(f"Decomposition Plot saved: {decomp_path}")

    return stats_summary

if __name__ == "__main__":
    run_latency_experiment()
