import time
import os
import requests
import json
import csv
import psutil
from concurrent.futures import ThreadPoolExecutor
from experiments.config.experiment_config import ExperimentConfig
from experiments.workloads.generator import WorkloadGenerator
from experiments.analysis.statistics import calculate_stats, generate_markdown_table
from experiments.plots.plotter import (
    plot_throughput_vs_load,
    plot_p95_vs_offered_load,
    plot_resource_usage
)

def send_request(req):
    src = req["source"]
    dst = req["destination"]
    req_id = req.get("request_id", "unknown")
    if src[0] < 19.05:
        url = "http://localhost:10000/custom_eta"
    elif src[1] < 72.85:
        url = "http://localhost:9000/custom_eta"
    else:
        url = "http://localhost:8000/custom_eta"

    t0 = time.perf_counter()
    try:
        res = requests.post(url, json={
            "source": src,
            "destination": dst,
            "food": req["food"],
            "rider": req["rider"],
            "traffic": req["traffic"]
        }, timeout=5.0)
        t_ms = (time.perf_counter() - t0) * 1000.0
        return req_id, True, t_ms, res.status_code
    except Exception as e:
        t_ms = (time.perf_counter() - t0) * 1000.0
        return req_id, False, t_ms, 500

def run_scalability_experiment(config=None, concurrency_levels=[1, 2, 4, 8, 16, 32, 64, 128], offered_loads=[1, 5, 10, 20, 50, 100, 200]):
    if not config:
        config = ExperimentConfig(name="scalability")

    results_dir = os.path.join("results", "phase3", "scalability")
    os.makedirs(results_dir, exist_ok=True)

    print("=== Executing System Scalability, Throughput & Concurrency Load Sweep ===")
    
    workload_path = "experiments/workloads/benchmark_workload.json"
    if not os.path.exists(workload_path):
        gen = WorkloadGenerator(seed=config.random_seed)
        gen.save_benchmark_workload(filepath=workload_path, count=1000)

    with open(workload_path, "r") as f:
        full_workload = json.load(f)

    process = psutil.Process(os.getpid())

    # 1. Concurrency Sweep
    print("\n--- Phase A: Concurrency Sweep (1 to 128 Workers) ---")
    raw_concurrency_records = []
    summary_concurrency = []

    for c in concurrency_levels:
        sample_count = max(100, c * 10)
        workload_sample = [full_workload[i % len(full_workload)] for i in range(sample_count)]
        print(f"Testing Concurrency Level: {c} workers ({sample_count} requests)...")

        t_start = time.perf_counter()
        cpu_start = process.cpu_percent(interval=None)

        with ThreadPoolExecutor(max_workers=c) as executor:
            results = list(executor.map(send_request, workload_sample))

        t_duration = time.perf_counter() - t_start
        cpu_pct = process.cpu_percent(interval=None)
        mem_mb = process.memory_info().rss / (1024 * 1024)

        rps = len(workload_sample) / max(0.001, t_duration)
        latencies = [lat for rid, ok, lat, status in results]
        succ_count = sum(1 for rid, ok, lat, status in results if ok)
        fail_count = len(results) - succ_count

        stats = calculate_stats(latencies)

        for rid, ok, lat, status in results:
            raw_concurrency_records.append({
                "concurrency": c,
                "request_id": rid,
                "latency_ms": round(lat, 3),
                "success": ok,
                "status_code": status
            })

        summary_concurrency.append({
            "concurrency": c,
            "request_count": len(workload_sample),
            "success_count": succ_count,
            "failure_count": fail_count,
            "achieved_rps": round(rps, 2),
            "p50_ms": stats["p50"],
            "p95_ms": stats["p95"],
            "p99_ms": stats["p99"],
            "mean_ms": stats["mean"],
            "cpu_percent": round(cpu_pct, 1),
            "ram_mb": round(mem_mb, 1)
        })

        print(f"  Concurrency {c:3d}: RPS={rps:6.2f}, P50={stats['p50']:6.2f}ms, P95={stats['p95']:6.2f}ms, P99={stats['p99']:6.2f}ms, CPU={cpu_pct:4.1f}%, RAM={mem_mb:5.1f}MB")

    # 2. Offered Load Sweep
    print("\n--- Phase B: Offered Load Sweep (1 to 200 req/sec) ---")
    raw_load_records = []
    summary_load = []

    for target_load in offered_loads:
        req_count = max(100, target_load * 3)
        workload_sample = [full_workload[i % len(full_workload)] for i in range(req_count)]
        
        # Paced execution targeting target_load rate
        interval_between_reqs = 1.0 / target_load if target_load > 0 else 0.0
        
        t_start = time.perf_counter()
        futures = []

        with ThreadPoolExecutor(max_workers=min(64, max(4, target_load))) as executor:
            for req in workload_sample:
                futures.append(executor.submit(send_request, req))
                if interval_between_reqs > 0:
                    time.sleep(interval_between_reqs * 0.95)

            results = [f.result() for f in futures]

        t_duration = time.perf_counter() - t_start
        achieved_rps = len(workload_sample) / max(0.001, t_duration)
        cpu_pct = process.cpu_percent(interval=None)
        mem_mb = process.memory_info().rss / (1024 * 1024)

        latencies = [lat for rid, ok, lat, status in results]
        succ_count = sum(1 for rid, ok, lat, status in results if ok)
        fail_count = len(results) - succ_count
        stats = calculate_stats(latencies)
        err_rate = (fail_count / len(workload_sample)) * 100.0

        for rid, ok, lat, status in results:
            raw_load_records.append({
                "offered_load": target_load,
                "request_id": rid,
                "latency_ms": round(lat, 3),
                "success": ok,
                "status_code": status
            })

        summary_load.append({
            "offered_load": target_load,
            "achieved_rps": round(achieved_rps, 2),
            "request_count": len(workload_sample),
            "success_count": succ_count,
            "failure_count": fail_count,
            "p50_ms": stats["p50"],
            "p95_ms": stats["p95"],
            "p99_ms": stats["p99"],
            "mean_ms": stats["mean"],
            "error_rate_pct": round(err_rate, 2),
            "cpu_percent": round(cpu_pct, 1),
            "ram_mb": round(mem_mb, 1)
        })

        print(f"  Target Load {target_load:3d} req/s -> Achieved {achieved_rps:6.2f} RPS, P50={stats['p50']:6.2f}ms, P95={stats['p95']:6.2f}ms, P99={stats['p99']:6.2f}ms, Errors={fail_count} ({err_rate:.1f}%)")

    # 3. Save Raw Data
    csv_c_path = os.path.join(results_dir, "scalability_raw_concurrency.csv")
    with open(csv_c_path, "w", newline="") as f:
        if raw_concurrency_records:
            writer = csv.DictWriter(f, fieldnames=list(raw_concurrency_records[0].keys()))
            writer.writeheader()
            writer.writerows(raw_concurrency_records)

    csv_l_path = os.path.join(results_dir, "scalability_raw_load.csv")
    with open(csv_l_path, "w", newline="") as f:
        if raw_load_records:
            writer = csv.DictWriter(f, fieldnames=list(raw_load_records[0].keys()))
            writer.writeheader()
            writer.writerows(raw_load_records)

    # 4. Generate Plots
    plot_throughput_vs_load(
        [item["offered_load"] for item in summary_load],
        {"EdgeSync Cluster": [item["achieved_rps"] for item in summary_load]},
        os.path.join(results_dir, "throughput_vs_load.png")
    )
    plot_p95_vs_offered_load(
        [item["offered_load"] for item in summary_load],
        {"EdgeSync Cluster": [item["p95_ms"] for item in summary_load]},
        os.path.join(results_dir, "p95_vs_offered_load.png")
    )
    plot_resource_usage(
        [item["concurrency"] for item in summary_concurrency],
        [item["cpu_percent"] for item in summary_concurrency],
        [item["ram_mb"] for item in summary_concurrency],
        os.path.join(results_dir, "resource_usage.png")
    )

    # 5. Generate Summary Markdown Tables
    headers_c = ["Concurrency", "Requests", "Success", "Failed", "Throughput (RPS)", "P50 (ms)", "P95 (ms)", "P99 (ms)", "CPU (%)", "RAM (MB)"]
    rows_c = [
        [item["concurrency"], item["request_count"], item["success_count"], item["failure_count"], item["achieved_rps"], item["p50_ms"], item["p95_ms"], item["p99_ms"], item["cpu_percent"], item["ram_mb"]]
        for item in summary_concurrency
    ]
    md_table_c = generate_markdown_table(headers_c, rows_c)

    headers_l = ["Offered Load (req/s)", "Achieved RPS", "Requests", "Success", "Failed", "P50 (ms)", "P95 (ms)", "P99 (ms)", "Error Rate (%)", "CPU (%)", "RAM (MB)"]
    rows_l = [
        [item["offered_load"], item["achieved_rps"], item["request_count"], item["success_count"], item["failure_count"], item["p50_ms"], item["p95_ms"], item["p99_ms"], item["error_rate_pct"], item["cpu_percent"], item["ram_mb"]]
        for item in summary_load
    ]
    md_table_l = generate_markdown_table(headers_l, rows_l)

    with open(os.path.join(results_dir, "scalability_summary.md"), "w") as f:
        f.write("# Scalability, Concurrency & Offered Load Sweep Summary\n\n")
        f.write("## Concurrency Sweep (1 to 128 Workers)\n\n" + md_table_c + "\n\n")
        f.write("## Offered Load Sweep (1 to 200 req/s)\n\n" + md_table_l + "\n")

    summary_json = {
        "concurrency_sweep": summary_concurrency,
        "offered_load_sweep": summary_load
    }
    with open(os.path.join(results_dir, "scalability_summary.json"), "w") as f:
        json.dump(summary_json, f, indent=2)

    print("\n--- Scalability Concurrency Summary Table ---")
    print(md_table_c)
    print("\n--- Scalability Offered Load Summary Table ---")
    print(md_table_l)

    return summary_json

if __name__ == "__main__":
    run_scalability_experiment()
