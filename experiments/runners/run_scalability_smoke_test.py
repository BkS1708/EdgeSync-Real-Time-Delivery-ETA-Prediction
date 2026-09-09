import sys
import os
import time
import json
import csv
import subprocess
import datetime
import hashlib
import random
import threading
from concurrent.futures import ThreadPoolExecutor
import requests
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from experiments.analysis.statistics import calculate_stats, generate_markdown_table

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

REGION_BOUNDS = {
    "EAST": {"lat": (19.06, 19.20), "lon": (72.86, 72.95)},
    "WEST": {"lat": (19.06, 19.20), "lon": (72.80, 72.84)},
    "CENTRAL": {"lat": (18.92, 19.04), "lon": (72.82, 72.95)}
}

FOOD_TYPES = ["pizza", "burger", "sandwich", "taco"]
RIDER_OPTIONS = ["Near (0.5-2 km)", "Medium (2-5 km)", "Far (5-8 km)"]
TRAFFIC_LEVELS = ["Low", "Medium", "High"]

def generate_point_in_region(region_name, rng):
    bounds = REGION_BOUNDS[region_name]
    lat = round(rng.uniform(bounds["lat"][0], bounds["lat"][1]), 6)
    lon = round(rng.uniform(bounds["lon"][0], bounds["lon"][1]), 6)
    return [lat, lon]

def generate_scalability_workload(count=20, seed=42, arch="edgesync_local"):
    rng = random.Random(seed)
    workload = []
    for i in range(count):
        req_id = f"req_{i+1:04d}"
        if arch == "centralized":
            src_reg = "EAST"
            dst_reg = "WEST" if (i % 2 == 0) else "EAST"
        elif arch == "edgesync_local":
            src_reg = "EAST"
            dst_reg = "EAST"
        elif arch == "edgesync_remote":
            src_reg = "EAST"
            dst_reg = "WEST"

        src_coord = generate_point_in_region(src_reg, rng)
        dst_coord = generate_point_in_region(dst_reg, rng)

        food = FOOD_TYPES[i % len(FOOD_TYPES)]
        rider = RIDER_OPTIONS[(i // 2) % len(RIDER_OPTIONS)]
        traffic = TRAFFIC_LEVELS[(i // 3) % len(TRAFFIC_LEVELS)]

        workload.append({
            "request_id": req_id,
            "source": src_coord,
            "destination": dst_coord,
            "source_region": src_reg,
            "dest_region": dst_reg,
            "is_local": (src_reg == dst_reg),
            "food": food,
            "rider": rider,
            "traffic": traffic
        })
    return workload

def compute_workload_hash(workload_data):
    serialized = json.dumps(workload_data, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

class ClusterManager:
    def __init__(self):
        self.procs = {}

    def start_node(self, region_name):
        port = {"EAST": 8000, "WEST": 9000, "CENTRAL": 10000}[region_name]
        try:
            r = requests.get(f"http://127.0.0.1:{port}/health", timeout=0.5)
            if r.status_code == 200:
                return True
        except Exception:
            pass

        env = os.environ.copy()
        env["EDGESYNC_BENCHMARK_MODE"] = "true"
        env["EDGESYNC_DOMAIN_DELAY"] = "false"
        env["EDGESYNC_NODE_HOST"] = "127.0.0.1"
        py_exec = sys.executable
        app_module = f"{region_name.lower()}:app"
        proc = subprocess.Popen([py_exec, "-m", "uvicorn", app_module, "--host", "127.0.0.1", "--port", str(port)], cwd=PROJECT_ROOT, env=env)
        self.procs[region_name] = proc

        for _ in range(20):
            try:
                r = requests.get(f"http://127.0.0.1:{port}/health", timeout=0.5)
                if r.status_code == 200:
                    return True
            except Exception:
                time.sleep(0.2)
        return False

    def ensure_all_running(self):
        for reg in ["EAST", "WEST", "CENTRAL"]:
            self.start_node(reg)

    def cleanup(self):
        for reg, proc in self.procs.items():
            if proc:
                try:
                    proc.terminate()
                except Exception:
                    pass

thread_local = threading.local()
def get_thread_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def execute_single_request(item):
    req, arch, concurrency, trial, is_warmup, wl_hash = item
    session = get_thread_session()
    target_url = "http://127.0.0.1:8000/custom_eta"

    if arch == "centralized":
        payload = {
            "source": req["source"], "destination": req["destination"],
            "food": req["food"], "rider": req["rider"], "traffic": req["traffic"],
            "partitioning_enabled": False, "delegation_enabled": False,
            "benchmark_mode": True, "domain_delay": False
        }
    else: # edgesync_local or edgesync_remote
        payload = {
            "source": req["source"], "destination": req["destination"],
            "food": req["food"], "rider": req["rider"], "traffic": req["traffic"],
            "partitioning_enabled": True, "delegation_enabled": True,
            "benchmark_mode": True, "domain_delay": False
        }

    t_start = time.perf_counter()
    start_time_iso = get_timestamp()
    success = False
    http_status = 0
    fallback_triggered = False
    t_total_ms = 0.0
    t_sys_ms = 0.0
    t_net_ms = 0.0
    t_dom_ms = 0.0

    try:
        res_raw = session.post(target_url, json=payload, timeout=10.0)
        t_end = time.perf_counter()
        t_total_ms = (t_end - t_start) * 1000.0
        http_status = res_raw.status_code
        if http_status == 200:
            res = res_raw.json()
            lat_info = res.get("latency_ms", {})
            t_sys_ms = lat_info.get("system", t_total_ms)
            t_net_ms = lat_info.get("network", 0.0)
            t_dom_ms = lat_info.get("computation", t_sys_ms)
            fallback_triggered = res.get("fallback_triggered", False)
            success = True
    except Exception as e:
        t_end = time.perf_counter()
        t_total_ms = (t_end - t_start) * 1000.0
        http_status = 500
        success = False

    end_time_iso = get_timestamp()

    return {
        "request_id": req["request_id"],
        "architecture": arch,
        "concurrency": concurrency,
        "trial": trial,
        "warmup": is_warmup,
        "timestamp": round(time.time(), 3),
        "start_time": start_time_iso,
        "end_time": end_time_iso,
        "total_latency_ms": round(t_total_ms, 3),
        "system_latency_ms": round(t_sys_ms, 3),
        "network_latency_ms": round(t_net_ms, 3),
        "domain_latency_ms": round(t_dom_ms, 3),
        "success": success,
        "http_status": http_status,
        "fallback_triggered": fallback_triggered,
        "region": req["source_region"],
        "target_region": req["dest_region"],
        "local_or_remote": "local" if req["is_local"] else "remote",
        "workload_hash": wl_hash
    }

def run_scalability_smoke_test():
    print("==========================================================")
    print("      EDGESYNC SCALABILITY EXPERIMENT — SMOKE TEST        ")
    print("==========================================================")
    print(f"Start Time: {get_timestamp()}\n")

    smoke_dir = os.path.join(PROJECT_ROOT, "results", "scalability", "smoke_test")
    raw_dir = os.path.join(smoke_dir, "raw")
    for d in [smoke_dir, raw_dir]:
        os.makedirs(d, exist_ok=True)

    cluster = ClusterManager()
    cluster.ensure_all_running()

    architectures = ["centralized", "edgesync_local", "edgesync_remote"]
    concurrency_levels = [1, 4, 16]
    trial = "trial1"

    summary_rows = []
    all_raw_data = []

    for arch in architectures:
        workload = generate_scalability_workload(count=20, seed=42, arch=arch)
        warmup_workload = generate_scalability_workload(count=10, seed=999, arch=arch)
        wl_hash = compute_workload_hash(workload)

        for c in concurrency_levels:
            print(f"[{get_timestamp()}] [SMOKE TEST] Running arch={arch} concurrency={c} (10 warmup + 20 measured)...", flush=True)

            # Warm-up phase (10 requests)
            warmup_items = [(req, arch, c, trial, True, wl_hash) for req in warmup_workload]
            with ThreadPoolExecutor(max_workers=c) as executor:
                list(executor.map(execute_single_request, warmup_items))

            # Measured phase (20 requests)
            measured_items = [(req, arch, c, trial, False, wl_hash) for req in workload]
            t_bench_start = time.perf_counter()
            with ThreadPoolExecutor(max_workers=c) as executor:
                measured_results = list(executor.map(execute_single_request, measured_items))
            t_bench_end = time.perf_counter()
            bench_duration = max(0.0001, t_bench_end - t_bench_start)

            # Write raw CSV
            csv_name = f"{arch}_c{c}_{trial}.csv"
            csv_path = os.path.join(raw_dir, csv_name)
            with open(csv_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(measured_results[0].keys()))
                writer.writeheader()
                writer.writerows(measured_results)

            all_raw_data.extend(measured_results)

            # Calculate statistics
            latencies = [r["total_latency_ms"] for r in measured_results]
            st = calculate_stats(latencies)
            succ_cnt = sum(1 for r in measured_results if r["success"])
            fail_cnt = len(measured_results) - succ_cnt
            avail_pct = round((succ_cnt / len(measured_results)) * 100.0, 2)
            throughput_rps = round(succ_cnt / bench_duration, 2)

            summary_rows.append({
                "architecture": arch,
                "concurrency": c,
                "trial": trial,
                "N": len(measured_results),
                "successful_requests": succ_cnt,
                "failed_requests": fail_cnt,
                "availability_pct": avail_pct,
                "throughput_rps": throughput_rps,
                "p50_ms": st["p50"],
                "p90_ms": st["p90"],
                "p95_ms": st["p95"],
                "p99_ms": st["p99"],
                "mean_ms": st["mean"],
                "stddev_ms": st["stddev"],
                "min_ms": st["min"],
                "max_ms": st["max"],
                "benchmark_duration_sec": round(bench_duration, 4)
            })

            print(f"  --> Completed {arch} (c={c}): Succ={succ_cnt}/20, P50={st['p50']}ms, P95={st['p95']}ms, Throughput={throughput_rps} req/s", flush=True)

    # Write summary.csv
    sum_csv_path = os.path.join(smoke_dir, "summary.csv")
    with open(sum_csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    # Validation Checks
    val_checks = []
    val_checks.append(("All 9 smoke test combinations executed", len(summary_rows) == 9))
    val_checks.append(("All 9 raw CSV files exist", len(os.listdir(raw_dir)) == 9))
    val_checks.append(("No failed requests across smoke test", sum(r["failed_requests"] for r in summary_rows) == 0))
    val_checks.append(("100% availability achieved", all(r["availability_pct"] == 100.0 for r in summary_rows)))
    val_checks.append(("Throughput values positive and non-zero", all(r["throughput_rps"] > 0 for r in summary_rows)))
    val_checks.append(("Plausible P50 latency (< 5ms at c=1, < 200ms at c=16)", all(r["p50_ms"] < 5.0 for r in summary_rows if r["concurrency"] == 1) and all(r["p50_ms"] < 200.0 for r in summary_rows)))

    all_passed = all(chk for name, chk in val_checks)

    # Generate SMOKE_TEST_REPORT.md
    report_path = os.path.join(smoke_dir, "SMOKE_TEST_REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# EdgeSync Scalability Experiment — Smoke Test Report\n\n")
        f.write(f"**Execution Date/Time:** `{get_timestamp()}`  \n")
        f.write(f"**Smoke Test Status:** `{'PASSED' if all_passed else 'FAILED'}`  \n")
        f.write(f"**Total Runs:** `9` (3 Architectures × 3 Concurrency Levels: 1, 4, 16)  \n")
        f.write(f"**Total Measured Requests:** `180` requests (20 per condition)  \n\n")
        f.write("---\n\n")

        f.write("## 1. Validation Summary\n\n")
        for name, chk in val_checks:
            f.write(f"- [{'x' if chk else ' '}] **{name}:** `{'PASS' if chk else 'FAIL'}`\n")
        f.write("\n")

        f.write("## 2. Smoke Test Results Table\n\n")
        headers = ["Architecture", "Concurrency", "N", "Success", "Avail (%)", "Throughput (req/s)", "P50 (ms)", "P95 (ms)", "P99 (ms)", "Mean (ms)"]
        rows = [[r["architecture"], r["concurrency"], r["N"], r["successful_requests"], f"{r['availability_pct']:.1f}%", f"{r['throughput_rps']:.2f}", f"{r['p50_ms']:.3f}", f"{r['p95_ms']:.3f}", f"{r['p99_ms']:.3f}", f"{r['mean_ms']:.3f}"] for r in summary_rows]
        f.write(generate_markdown_table(headers, rows) + "\n\n")

        f.write("## 3. Pre-Flight Conclusion\n\n")
        if all_passed:
            f.write("All pre-flight validation checks passed. The experimental infrastructure, thread pooling, socket sessions, decomposed latency tracking, and throughput measurement are functioning reliably and are approved for the full 6,300-request scalability experiment.\n")
        else:
            f.write("Smoke test encountered failures. Resolve all flagged issues before launching the full experiment.\n")

    print(f"\n[{get_timestamp()}] Smoke Test Complete! Status: {'PASSED' if all_passed else 'FAILED'}")
    print(f"[{get_timestamp()}] Report written to: {report_path}\n")

    cluster.cleanup()
    return all_passed

if __name__ == "__main__":
    success = run_scalability_smoke_test()
    if not success:
        sys.exit(1)
