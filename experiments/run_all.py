import sys
import os
import platform
import time
import json
import subprocess
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from experiments.config.experiment_config import ExperimentConfig
from experiments.workloads.generator import WorkloadGenerator
from experiments.runners.run_latency_experiment import run_latency_experiment
from experiments.runners.run_scalability_experiment import run_scalability_experiment
from experiments.runners.run_gossip_experiment import run_gossip_experiment
from experiments.runners.run_fault_experiment import run_fault_experiment
from experiments.runners.run_ablation_experiment import run_ablation_experiment
from experiments.runners.run_partition_experiment import run_partition_experiment
from experiments.validate_results import validate_phase3_results

def detect_machine_info():
    info = {
        "python_version": sys.version,
        "os_platform": platform.platform(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count()
    }
    try:
        import torch
        info["pytorch_version"] = torch.__version__
        info["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            info["gpu_name"] = torch.cuda.get_device_name(0)
    except ImportError:
        info["pytorch_version"] = "Not Installed"
        info["cuda_available"] = False
    return info

def ensure_servers_running():
    print("Verifying microservice health on ports 8000, 9000, 10000...")
    ports = {"EAST": 8000, "WEST": 9000, "CENTRAL": 10000}
    processes = []
    
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    for name, port in ports.items():
        try:
            r = requests.get(f"http://localhost:{port}/health", timeout=1.0)
            if r.status_code == 200:
                print(f"  [OK] {name} Node is online at port {port}.")
                continue
        except Exception:
            pass

        print(f"  [STARTING] Launching {name} microservice on port {port}...")
        py_exec = sys.executable
        app_module = f"{name.lower()}:app"
        proc = subprocess.Popen([py_exec, "-m", "uvicorn", app_module, "--port", str(port)], cwd=root_dir)
        processes.append(proc)

    if processes:
        print("Waiting 4 seconds for microservices to initialize...")
        time.sleep(4.0)

    # Double check health
    for name, port in ports.items():
        for attempt in range(5):
            try:
                r = requests.get(f"http://localhost:{port}/health", timeout=1.0)
                if r.status_code == 200:
                    print(f"  [VERIFIED] {name} Node is responding (port {port}).")
                    break
            except Exception:
                time.sleep(1.0)

    return processes

def run_all_experiments():
    print("==========================================================")
    print("   EDGESYNC IEEE PERCOM PHASE 3 VALIDATED EXPERIMENTAL SUITE")
    print("==========================================================\n")

    machine_info = detect_machine_info()
    print("Detected System Environment:")
    print(f"  OS: {machine_info['os_platform']}")
    print(f"  Python: {machine_info['python_version'].split()[0]}")
    print(f"  CPU Cores: {machine_info['cpu_count']}")
    print(f"  CUDA Available: {machine_info['cuda_available']}\n")

    spawned_procs = ensure_servers_running()

    # Ensure results/phase3 directory structure
    phase3_dir = os.path.join("results", "phase3")
    os.makedirs(phase3_dir, exist_ok=True)

    # Generate single benchmark workload & SHA-256 hash (1000 requests)
    workload_path = "experiments/workloads/benchmark_workload.json"
    gen = WorkloadGenerator(seed=42)
    gen.save_benchmark_workload(filepath=workload_path, count=1000)
    workload_hash = WorkloadGenerator.get_workload_hash(workload_path)

    cfg = ExperimentConfig(name="percom_master_run", random_seed=42)
    master_results = {
        "experiment_id": f"percom_phase3_run_{int(time.time())}",
        "timestamp": time.time(),
        "seed": 42,
        "workload_hash": workload_hash,
        "machine_info": machine_info
    }

    try:
        # 1. Matched Decision Latency Experiment (N=1000 matched requests, 50 warm-up)
        print("\n----------------------------------------------------------")
        latency_res = run_latency_experiment(config=cfg, num_requests=1000, warmup_count=50)
        master_results["latency_experiment"] = latency_res

        # 2. Scalability, Concurrency & Offered Load Sweep
        print("\n----------------------------------------------------------")
        scalability_res = run_scalability_experiment(config=cfg, concurrency_levels=[1, 2, 4, 8, 16, 32, 64, 128], offered_loads=[1, 5, 10, 20, 50, 100, 200])
        master_results["scalability_experiment"] = scalability_res

        # 3. Gossip Protocol & Topology Trade-offs
        print("\n----------------------------------------------------------")
        gossip_res = run_gossip_experiment(config=cfg)
        master_results["gossip_experiment"] = gossip_res

        # 4. Controlled Fault Matrix & Recovery Timeline
        print("\n----------------------------------------------------------")
        fault_res = run_fault_experiment(config=cfg)
        master_results["fault_experiment"] = fault_res

        # 5. Component Ablation Studies (Pure System Overhead)
        print("\n----------------------------------------------------------")
        ablation_res = run_ablation_experiment(config=cfg, count=200)
        master_results["ablation_experiment"] = ablation_res

        # 6. Spatial Locality & Hotspot Partitioning
        print("\n----------------------------------------------------------")
        partition_res = run_partition_experiment(config=cfg)
        master_results["partitioning_experiment"] = partition_res

        # Save Metadata & Reproducibility Package
        metadata_file = os.path.join(phase3_dir, "experiment_metadata.json")
        master_file = os.path.join(phase3_dir, "master_experiment_summary.json")

        with open(metadata_file, "w") as f:
            json.dump(master_results, f, indent=2)

        with open(master_file, "w") as f:
            json.dump(master_results, f, indent=2)

        print("\n==========================================================")
        print("   ALL PHASE 3 EXPERIMENTS EXECUTED SUCCESSFULLY!         ")
        print(f"   Master Summary Saved To: {master_file}                 ")
        print(f"   Metadata Package Saved To: {metadata_file}             ")
        print("==========================================================")

        # 7. Run Data Integrity Validation Checker
        print("\nRunning Scientific Data Integrity & Audit Checker...")
        validation_passed = validate_phase3_results(results_dir=phase3_dir)
        if not validation_passed:
            print("WARNING: Data validation detected discrepancies. Please check output above.")

    finally:
        if spawned_procs:
            print("\nCleaning up spawned microservice background processes...")
            for proc in spawned_procs:
                try:
                    proc.terminate()
                except Exception:
                    pass

if __name__ == "__main__":
    run_all_experiments()
