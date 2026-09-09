import os
import glob
import csv
import json
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
raw_dir = os.path.join(PROJECT_ROOT, "results", "fault_tolerance", "raw")
debug_dir = os.path.join(PROJECT_ROOT, "results", "fault_tolerance", "debug")
os.makedirs(debug_dir, exist_ok=True)

csv_files = sorted(glob.glob(os.path.join(raw_dir, "*.csv")))
print(f"Found {len(csv_files)} CSV files in {raw_dir}")

audit_rows = []
for fpath in csv_files:
    fname = os.path.basename(fpath)
    with open(fpath, "r", newline="") as f:
        reader = list(csv.DictReader(f))
    total = len(reader)
    status_counts = {}
    success_cnt = 0
    fail_cnt = 0
    fb_cnt = 0
    phases = {
        "baseline": {"total": 0, "succ": 0, "fb": 0},
        "failure": {"total": 0, "succ": 0, "fb": 0},
        "recovery": {"total": 0, "succ": 0, "fb": 0}
    }
    latencies = []
    
    for r in reader:
        st = r.get("http_status", "N/A")
        status_counts[st] = status_counts.get(st, 0) + 1
        is_succ = (str(r.get("success", "")).lower() == "true")
        is_fb = (str(r.get("fallback_triggered", "")).lower() == "true")
        if is_succ:
            success_cnt += 1
        else:
            fail_cnt += 1
        if is_fb:
            fb_cnt += 1
        
        ph = r.get("failure_state", "unknown")
        if ph in phases:
            phases[ph]["total"] += 1
            if is_succ:
                phases[ph]["succ"] += 1
            if is_fb:
                phases[ph]["fb"] += 1
        
        try:
            latencies.append(float(r.get("total_latency_ms", 0)))
        except Exception:
            pass
            
    p50 = round(float(np.percentile(latencies, 50)), 3) if latencies else 0.0
    p95 = round(float(np.percentile(latencies, 95)), 3) if latencies else 0.0
    mean_lat = round(float(np.mean(latencies)), 3) if latencies else 0.0
    
    scenario = reader[0].get("scenario", "N/A") if reader else "N/A"
    trial_id = reader[0].get("trial_id", "N/A") if reader else "N/A"

    audit_rows.append({
        "filename": fname,
        "scenario": scenario,
        "trial_id": trial_id,
        "total_requests": total,
        "successful_requests": success_cnt,
        "failed_requests": fail_cnt,
        "availability_pct": round(success_cnt / max(1, total) * 100.0, 2),
        "http_status_dist": json.dumps(status_counts),
        "fallback_activations": fb_cnt,
        "fallback_rate_pct": round(fb_cnt / max(1, total) * 100.0, 2),
        "baseline_succ": phases["baseline"]["succ"],
        "baseline_total": phases["baseline"]["total"],
        "failure_succ": phases["failure"]["succ"],
        "failure_total": phases["failure"]["total"],
        "failure_fb": phases["failure"]["fb"],
        "recovery_succ": phases["recovery"]["succ"],
        "recovery_total": phases["recovery"]["total"],
        "mean_latency_ms": mean_lat,
        "p50_latency_ms": p50,
        "p95_latency_ms": p95
    })

out_csv = os.path.join(debug_dir, "RAW_DATA_AUDIT.csv")
with open(out_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(audit_rows[0].keys()))
    writer.writeheader()
    writer.writerows(audit_rows)

print(f"Generated {out_csv} with {len(audit_rows)} rows.")
for r in audit_rows:
    print(f"{r['filename']:<42} Total={r['total_requests']} Succ={r['successful_requests']} Fail={r['failed_requests']} HTTP={r['http_status_dist']} FB={r['fallback_activations']}")
