import os
import sys
import glob
import csv
import json
import numpy as np
from scipy.stats import wilcoxon

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
raw_dir = os.path.join(PROJECT_ROOT, "results", "scalability", "raw")
stats_dir = os.path.join(PROJECT_ROOT, "results", "scalability", "statistics")

csv_files = sorted(glob.glob(os.path.join(raw_dir, "*.csv")))
print(f"Total raw CSV files found: {len(csv_files)}")

# 1. Inspect all 63 raw CSV files
architectures = ["centralized", "edgesync_local", "edgesync_remote"]
concurrencies = [1, 2, 4, 8, 16, 32, 64]
trials = ["trial1", "trial2", "trial3"]

expected_files = []
for arch in architectures:
    for c in concurrencies:
        for tr in trials:
            expected_files.append(f"{arch}_c{c}_{tr}.csv")

print(f"Total expected files: {len(expected_files)}")
missing_files = [f for f in expected_files if not os.path.exists(os.path.join(raw_dir, f))]
print(f"Missing files: {missing_files}")

mandatory_cols = [
    "request_id", "architecture", "concurrency", "trial", "warmup",
    "timestamp", "start_time", "end_time", "total_latency_ms",
    "system_latency_ms", "network_latency_ms", "domain_latency_ms",
    "success", "http_status", "fallback_triggered", "region",
    "target_region", "local_or_remote", "workload_hash"
]

all_records = []
audit_by_file = {}
malformed_files = []
nan_found = []
duplicate_ids = []

for fpath in csv_files:
    fname = os.path.basename(fpath)
    with open(fpath, "r", newline="") as f:
        reader = list(csv.DictReader(f))
    
    if len(reader) != 100:
        malformed_files.append((fname, f"row_count={len(reader)}"))
        
    req_ids = set()
    for idx, r in enumerate(reader):
        for col in mandatory_cols:
            if col not in r:
                malformed_files.append((fname, f"missing_col={col}"))
            val = r.get(col, "")
            if val is None or val == "" or str(val).lower() == "nan":
                nan_found.append((fname, col, idx))
                
        rid = r["request_id"]
        if rid in req_ids:
            duplicate_ids.append((fname, rid))
        req_ids.add(rid)
        
        # Type conversions
        r["total_latency_ms"] = float(r["total_latency_ms"])
        r["system_latency_ms"] = float(r["system_latency_ms"])
        r["network_latency_ms"] = float(r["network_latency_ms"])
        r["domain_latency_ms"] = float(r["domain_latency_ms"])
        r["success"] = (str(r["success"]).lower() == "true")
        r["fallback_triggered"] = (str(r["fallback_triggered"]).lower() == "true")
        r["http_status"] = int(r["http_status"])
        r["concurrency"] = int(r["concurrency"])
        r["timestamp"] = float(r["timestamp"])
        r["warmup"] = (str(r["warmup"]).lower() == "true")
        all_records.append(r)
        
    succ = sum(1 for r in reader if r["success"])
    fail = len(reader) - succ
    lats = [r["total_latency_ms"] for r in reader]
    timestamps = [r["timestamp"] for r in reader]
    dur = max(0.001, max(timestamps) - min(timestamps)) if len(timestamps) > 1 else 0.1
    recalc_rps = round(succ / dur, 2)
    
    audit_by_file[fname] = {
        "N": len(reader),
        "success": succ,
        "failed": fail,
        "availability_pct": round(succ / len(reader) * 100.0, 2),
        "duration_sec": round(dur, 4),
        "recalc_throughput_rps": recalc_rps,
        "p50": round(float(np.percentile(lats, 50)), 3),
        "p90": round(float(np.percentile(lats, 90)), 3),
        "p95": round(float(np.percentile(lats, 95)), 3),
        "p99": round(float(np.percentile(lats, 99)), 3),
        "mean": round(float(np.mean(lats)), 3),
        "std": round(float(np.std(lats)), 3)
    }

print("\n--- PHASE 1 SUMMARY ---")
print(f"Total files: {len(csv_files)}")
print(f"Malformed files: {len(malformed_files)}")
print(f"NaN values found: {len(nan_found)}")
print(f"Duplicate IDs: {len(duplicate_ids)}")
print(f"Total measured observations loaded: {len(all_records)}")
print(f"All warmup==False: {all(not r['warmup'] for r in all_records)}")
print(f"Total successful: {sum(1 for r in all_records if r['success'])} / {len(all_records)}")

# 2. Compare recalculations with latency_statistics.csv and throughput_statistics.csv
with open(os.path.join(stats_dir, "latency_statistics.csv"), "r") as f:
    rep_latency = list(csv.DictReader(f))

with open(os.path.join(stats_dir, "throughput_statistics.csv"), "r") as f:
    rep_throughput = list(csv.DictReader(f))

with open(os.path.join(stats_dir, "trial_statistics.csv"), "r") as f:
    rep_trial = list(csv.DictReader(f))

print("\n--- PHASE 4 & 5 VERIFICATION ---")
latency_diffs = []
for arch in architectures:
    for c in concurrencies:
        sub = [r for r in all_records if r["architecture"] == arch and r["concurrency"] == c]
        lats = [r["total_latency_ms"] for r in sub]
        rec_p50 = round(float(np.percentile(lats, 50)), 3)
        rec_p95 = round(float(np.percentile(lats, 95)), 3)
        rec_p99 = round(float(np.percentile(lats, 99)), 3)
        rec_mean = round(float(np.mean(lats)), 3)
        
        rep_row = [r for r in rep_latency if r["architecture"] == arch and int(r["concurrency"]) == c][0]
        rep_p50 = float(rep_row["total_p50_ms"])
        rep_p95 = float(rep_row["total_p95_ms"])
        rep_p99 = float(rep_row["total_p99_ms"])
        rep_mean = float(rep_row["total_mean_ms"])
        
        diff_p50 = abs(rec_p50 - rep_p50)
        diff_p95 = abs(rec_p95 - rep_p95)
        diff_p99 = abs(rec_p99 - rep_p99)
        diff_mean = abs(rec_mean - rep_mean)
        latency_diffs.append((arch, c, diff_p50, diff_p95, diff_p99, diff_mean))

max_lat_diff = max(max(d[2:]) for d in latency_diffs)
print(f"Max absolute discrepancy in Latency Statistics vs Recalculated: {max_lat_diff} ms")

# 3. Paired Statistical Test Audit
with open(os.path.join(stats_dir, "paired_tests.csv"), "r") as f:
    rep_paired = list(csv.DictReader(f))

print("\n--- PHASE 6 STATISTICAL TEST AUDIT ---")
for p_row in rep_paired:
    c = int(p_row["concurrency"])
    arch_a = p_row["arch_a"]
    arch_b = p_row["arch_b"]
    comp = p_row["comparison"]
    
    # Check request-level matching by (trial, request_id)
    sub_a = { (r["trial"], r["request_id"]): r["total_latency_ms"] for r in all_records if r["architecture"] == arch_a and r["concurrency"] == c }
    sub_b = { (r["trial"], r["request_id"]): r["total_latency_ms"] for r in all_records if r["architecture"] == arch_b and r["concurrency"] == c }
    
    common_keys = sorted(list(set(sub_a.keys()).intersection(set(sub_b.keys()))))
    arr_a = [sub_a[k] for k in common_keys]
    arr_b = [sub_b[k] for k in common_keys]
    
    res = wilcoxon(arr_a, arr_b)
    stat = round(float(res.statistic), 2)
    pval = float(res.pvalue)
    
    rep_stat = float(p_row["wilcoxon_stat"])
    rep_raw_p = float(p_row["raw_p_value"])
    
    print(f"c={c:2d} {comp:<32} N={len(common_keys)} Stat={stat} (rep {rep_stat}) p={pval:.4e} (rep {rep_raw_p:.4e})")
