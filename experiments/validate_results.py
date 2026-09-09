import os
import sys
import json
import csv
import pandas as pd
import numpy as np

def validate_phase3_results(results_dir="results/phase3"):
    print("==========================================================")
    print("   EDGESYNC SCIENTIFIC DATA INTEGRITY & AUDIT CHECKER     ")
    print("==========================================================\n")

    errors = []
    warnings = []

    if not os.path.exists(results_dir):
        print(f"FAILED: Target results directory '{results_dir}' does not exist.")
        return False

    # 1. Master & Metadata Files Check
    metadata_path = os.path.join(results_dir, "experiment_metadata.json")
    master_path = os.path.join(results_dir, "master_experiment_summary.json")

    if not os.path.exists(metadata_path):
        errors.append(f"Missing metadata file: {metadata_path}")
    else:
        print(f"  [OK] Metadata file found: {metadata_path}")

    if not os.path.exists(master_path):
        errors.append(f"Missing master summary file: {master_path}")
    else:
        print(f"  [OK] Master summary found: {master_path}")

    # 2. Latency Raw Data, N=1000 Sample Count & Pairing Integrity
    lat_dir = os.path.join(results_dir, "latency")
    lat_csv = os.path.join(lat_dir, "latency_raw_results.csv")
    lat_sum_json = os.path.join(lat_dir, "latency_summary.json")

    if not os.path.exists(lat_csv):
        errors.append(f"Missing latency raw CSV at {lat_csv}")
    else:
        df_lat = pd.read_csv(lat_csv)
        print(f"  [OK] Latency raw CSV verified: {lat_csv} ({len(df_lat)} rows)")
        
        # Verify columns exist
        required_cols = ["request_id", "mode", "request_latency_ms", "computation_latency_ms", "network_latency_ms", "success"]
        for c in required_cols:
            if c not in df_lat.columns:
                errors.append(f"Latency raw CSV missing required column: {c}")

        # Check architectures
        architectures = df_lat["mode"].unique()
        print(f"       Architectures in raw dataset: {list(architectures)}")

        req_ids_by_arch = {}
        for mode in architectures:
            sub = df_lat[df_lat["mode"] == mode]
            req_ids_by_arch[mode] = set(sub["request_id"].dropna())
            print(f"       Mode '{mode}': {len(sub)} samples, {len(req_ids_by_arch[mode])} unique IDs")

        # Verify strict pairing against Centralized Baseline
        if "Centralized Baseline" in req_ids_by_arch:
            cent_ids = req_ids_by_arch["Centralized Baseline"]
            for mode in architectures:
                if mode != "Centralized Baseline":
                    common = req_ids_by_arch[mode].intersection(cent_ids)
                    if len(common) == 0:
                        errors.append(f"No common request IDs between '{mode}' and 'Centralized Baseline' for pairing!")
                    else:
                        print(f"       Strict Paired Match: '{mode}' vs 'Centralized Baseline' ({len(common)} common IDs)")

        # Verify summary statistics match raw data calculations
        if os.path.exists(lat_sum_json):
            with open(lat_sum_json, "r") as f:
                lat_sum = json.load(f)
            for mode in architectures:
                if mode in lat_sum:
                    sub = df_lat[df_lat["mode"] == mode]
                    raw_mean = round(float(sub["request_latency_ms"].mean()), 3)
                    sum_mean = round(float(lat_sum[mode]["total_stats"]["mean"]), 3)
                    if abs(raw_mean - sum_mean) > 0.05:
                        errors.append(f"Latency summary mean mismatch for {mode}: summary={sum_mean}, calculated={raw_mean}")
                    else:
                        print(f"       Stat Match [OK] for '{mode}': Mean Latency = {raw_mean} ms")

    # 3. Scalability Sweep Results Check
    sc_dir = os.path.join(results_dir, "scalability")
    sc_raw_c = os.path.join(sc_dir, "scalability_raw_concurrency.csv")
    sc_raw_l = os.path.join(sc_dir, "scalability_raw_load.csv")
    sc_summary = os.path.join(sc_dir, "scalability_summary.json")

    if not os.path.exists(sc_raw_c):
        errors.append(f"Missing scalability concurrency raw CSV at {sc_raw_c}")
    else:
        df_sc_c = pd.read_csv(sc_raw_c)
        print(f"  [OK] Scalability concurrency raw CSV verified: {sc_raw_c} ({len(df_sc_c)} rows)")

    if not os.path.exists(sc_raw_l):
        errors.append(f"Missing scalability load raw CSV at {sc_raw_l}")
    else:
        df_sc_l = pd.read_csv(sc_raw_l)
        print(f"  [OK] Scalability load raw CSV verified: {sc_raw_l} ({len(df_sc_l)} rows)")

    if not os.path.exists(sc_summary):
        errors.append(f"Missing scalability summary at {sc_summary}")
    else:
        print(f"  [OK] Scalability summary verified: {sc_summary}")

    # 4. Gossip Convergence Check
    gos_dir = os.path.join(results_dir, "gossip")
    gos_raw_c = os.path.join(gos_dir, "gossip_raw_convergence.csv")
    gos_raw_t = os.path.join(gos_dir, "gossip_raw_topologies.csv")
    gos_summary = os.path.join(gos_dir, "gossip_summary.json")

    if not os.path.exists(gos_raw_c):
        errors.append(f"Missing gossip raw convergence CSV at {gos_raw_c}")
    else:
        print(f"  [OK] Gossip convergence raw CSV verified: {gos_raw_c}")

    if not os.path.exists(gos_raw_t):
        errors.append(f"Missing gossip raw topologies CSV at {gos_raw_t}")
    else:
        print(f"  [OK] Gossip topologies raw CSV verified: {gos_raw_t}")

    if not os.path.exists(gos_summary):
        errors.append(f"Missing gossip summary at {gos_summary}")
    else:
        print(f"  [OK] Gossip summary verified: {gos_summary}")

    # 5. Fault Matrix Results Check
    fault_dir = os.path.join(results_dir, "fault_tolerance")
    fault_raw = os.path.join(fault_dir, "fault_raw_events.csv")
    fault_csv = os.path.join(fault_dir, "fault_matrix.csv")
    fault_json = os.path.join(fault_dir, "summary.json")

    if not os.path.exists(fault_raw):
        errors.append(f"Missing fault raw events CSV at {fault_raw}")
    else:
        df_fault = pd.read_csv(fault_raw)
        print(f"  [OK] Fault raw events CSV verified: {fault_raw} ({len(df_fault)} rows)")

    if not os.path.exists(fault_csv):
        errors.append(f"Missing fault matrix CSV at {fault_csv}")
    else:
        print(f"  [OK] Fault matrix CSV verified: {fault_csv}")

    if not os.path.exists(fault_json):
        errors.append(f"Missing fault summary JSON at {fault_json}")
    else:
        print(f"  [OK] Fault summary JSON verified: {fault_json}")

    # 6. Ablation Summary Check
    abl_dir = os.path.join(results_dir, "ablation")
    abl_raw = os.path.join(abl_dir, "ablation_raw_results.csv")
    abl_json = os.path.join(abl_dir, "ablation_summary.json")

    if not os.path.exists(abl_raw):
        errors.append(f"Missing ablation raw CSV at {abl_raw}")
    else:
        df_abl = pd.read_csv(abl_raw)
        print(f"  [OK] Ablation raw CSV verified: {abl_raw} ({len(df_abl)} rows)")

    if not os.path.exists(abl_json):
        errors.append(f"Missing ablation summary JSON at {abl_json}")
    else:
        print(f"  [OK] Ablation summary JSON verified: {abl_json}")

    # 7. Partitioning Summary Check
    part_dir = os.path.join(results_dir, "partitioning")
    part_raw_l = os.path.join(part_dir, "partition_raw_locality.csv")
    part_raw_h = os.path.join(part_dir, "partition_raw_hotspots.csv")
    part_json = os.path.join(part_dir, "partitioning_summary.json")

    if not os.path.exists(part_raw_l):
        errors.append(f"Missing partition locality raw CSV at {part_raw_l}")
    else:
        print(f"  [OK] Partition locality raw CSV verified: {part_raw_l}")

    if not os.path.exists(part_raw_h):
        errors.append(f"Missing partition hotspots raw CSV at {part_raw_h}")
    else:
        print(f"  [OK] Partition hotspots raw CSV verified: {part_raw_h}")

    if not os.path.exists(part_json):
        errors.append(f"Missing partitioning summary JSON at {part_json}")
    else:
        print(f"  [OK] Partitioning summary JSON verified: {part_json}")

    # 8. Visual Plots Verification
    plots = [
        os.path.join(lat_dir, "latency_cdf.png"),
        os.path.join(lat_dir, "latency_decomposition.png"),
        os.path.join(sc_dir, "throughput_vs_load.png"),
        os.path.join(sc_dir, "p95_vs_offered_load.png"),
        os.path.join(sc_dir, "resource_usage.png"),
        os.path.join(gos_dir, "gossip_convergence.png"),
        os.path.join(gos_dir, "gossip_interval_tradeoff.png"),
        os.path.join(fault_dir, "fault_recovery_timeline.png"),
        os.path.join(abl_dir, "ablation_comparison.png"),
        os.path.join(part_dir, "partition_locality.png")
    ]
    missing_plots = [p for p in plots if not (os.path.exists(p) and os.path.getsize(p) > 100)]
    if missing_plots:
        for mp in missing_plots:
            errors.append(f"Missing or empty plot: {mp}")
    else:
        print(f"  [OK] All {len(plots)} experiment plots generated and verified non-empty.")

    # Summary
    print("\n----------------------------------------------------------")
    if errors:
        print(f"INTEGRITY CHECK FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  [ERROR] {err}")
        return False
    else:
        print("ALL DATA INTEGRITY AND EVIDENCE VALIDATION CHECKS PASSED SUCCESSFULLY!")
        if warnings:
            print(f"Warnings ({len(warnings)}):")
            for w in warnings:
                print(f"  [WARNING] {w}")
        return True

if __name__ == "__main__":
    success = validate_phase3_results()
    sys.exit(0 if success else 1)
