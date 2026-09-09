import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

def plot_latency_cdf(data_dict, output_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    for i, (label, latencies) in enumerate(data_dict.items()):
        if not latencies:
            continue
        sorted_lats = sorted(latencies)
        cdf = [j / len(sorted_lats) for j in range(1, len(sorted_lats) + 1)]
        color = colors[i % len(colors)]
        ax.plot(sorted_lats, cdf, label=label, linewidth=2, color=color)

    ax.set_title("Decision Latency Cumulative Distribution Function (CDF)", fontsize=13, fontweight='bold')
    ax.set_xlabel("Response Latency (ms)", fontsize=11)
    ax.set_ylabel("Cumulative Probability P(X <= x)", fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right", frameon=True)
    ax.grid(True, linestyle='--', alpha=0.6)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_latency_breakdown(categories, breakdown_dict, output_path):
    """
    breakdown_dict: {"Routing": [ms], "Network": [ms], "Compute": [ms]}
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    bottom = [0.0] * len(categories)
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f']

    for i, (component, values) in enumerate(breakdown_dict.items()):
        ax.bar(categories, values, bottom=bottom, label=component, color=colors[i % len(colors)], width=0.5)
        bottom = [b + v for b, v in zip(bottom, values)]

    ax.set_title("End-to-End Latency Decomposition Breakdown", fontsize=13, fontweight='bold')
    ax.set_ylabel("Time (ms)", fontsize=11)
    ax.legend(loc="upper left", frameon=True)
    ax.grid(True, linestyle='--', alpha=0.6)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_throughput_vs_load(offered_loads, throughput_dict, output_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    for label, rps_list in throughput_dict.items():
        ax.plot(offered_loads, rps_list, marker='o', linewidth=2, label=label)

    ax.set_title("Throughput vs Offered Request Rate", fontsize=13, fontweight='bold')
    ax.set_xlabel("Offered Request Rate (req/sec)", fontsize=11)
    ax.set_ylabel("Achieved Throughput (req/sec)", fontsize=11)
    ax.legend(loc="upper left", frameon=True)
    ax.grid(True, linestyle='--', alpha=0.6)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_p95_vs_offered_load(offered_loads, p95_dict, output_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    for label, p95_list in p95_dict.items():
        ax.plot(offered_loads, p95_list, marker='s', linewidth=2, label=label)

    ax.set_title("P95 Latency vs Offered Load", fontsize=13, fontweight='bold')
    ax.set_xlabel("Offered Request Rate (req/sec)", fontsize=11)
    ax.set_ylabel("P95 Decision Latency (ms)", fontsize=11)
    ax.legend(loc="upper left", frameon=True)
    ax.grid(True, linestyle='--', alpha=0.6)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_gossip_convergence(time_list, node_states_dict, output_path):
    fig, ax = plt.subplots(figsize=(8, 5))

    for node_name, avgs in node_states_dict.items():
        ax.plot(time_list, avgs, label=f"{node_name} Node State", linewidth=2)

    ax.set_title("Gossip State Convergence Over Time", fontsize=13, fontweight='bold')
    ax.set_xlabel("Time (Seconds)", fontsize=11)
    ax.set_ylabel("Running Average ETA (Minutes)", fontsize=11)
    ax.legend(loc="best", frameon=True)
    ax.grid(True, linestyle='--', alpha=0.6)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_gossip_interval_tradeoff(intervals, convergence_times, network_bytes, output_path):
    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.set_xlabel("Gossip Interval (Seconds)", fontsize=11)
    ax1.set_ylabel("Convergence Time (Seconds)", color='#2980b9', fontsize=11)
    ax1.plot(intervals, convergence_times, color='#2980b9', marker='o', linewidth=2, label="Convergence Time")
    ax1.tick_params(axis='y', labelcolor='#2980b9')

    ax2 = ax1.twinx()
    ax2.set_ylabel("Synchronization Traffic (KB/sec)", color='#e67e22', fontsize=11)
    ax2.plot(intervals, [b / 1024.0 for b in network_bytes], color='#e67e22', marker='s', linestyle='--', linewidth=2, label="Traffic")
    ax2.tick_params(axis='y', labelcolor='#e67e22')

    plt.title("Gossip Interval Trade-off: Convergence vs Overhead", fontsize=13, fontweight='bold')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_fault_recovery_timeline(time_list, success_list, failure_list, output_path):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(time_list, success_list, label="Successful Requests (HTTP 200)", color='green', linewidth=2)
    ax.plot(time_list, failure_list, label="Failed Requests (HTTP 500/Timeout)", color='red', linewidth=2)

    ax.set_title("Fault Tolerance & Recovery Timeline", fontsize=13, fontweight='bold')
    ax.set_xlabel("Timeline (Seconds)", fontsize=11)
    ax.set_ylabel("Requests Per Second", fontsize=11)
    ax.legend(loc="upper right", frameon=True)
    ax.grid(True, linestyle='--', alpha=0.6)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_network_latency_sensitivity(profile_labels, p95_latencies, output_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(profile_labels, p95_latencies, marker='D', color='#8e44ad', linewidth=2)
    ax.set_title("Network Latency Sensitivity Profile", fontsize=13, fontweight='bold')
    ax.set_xlabel("Network Profile (Injected Latency)", fontsize=11)
    ax.set_ylabel("P95 Decision Latency (ms)", fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.6)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_partition_locality(locality_percentages, cross_region_rates, latencies, output_path):
    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.set_xlabel("Spatial Locality Ratio (% Intra-Region)", fontsize=11)
    ax1.set_ylabel("Cross-Region Request Rate (%)", color='#c0392b', fontsize=11)
    ax1.plot(locality_percentages, cross_region_rates, color='#c0392b', marker='o', linewidth=2)
    ax1.tick_params(axis='y', labelcolor='#c0392b')

    ax2 = ax1.twinx()
    ax2.set_ylabel("Mean Decision Latency (ms)", color='#27ae60', fontsize=11)
    ax2.plot(locality_percentages, latencies, color='#27ae60', marker='s', linestyle='--', linewidth=2)
    ax2.tick_params(axis='y', labelcolor='#27ae60')

    plt.title("Impact of Geographic Locality on Latency and Cross-Region Traffic", fontsize=13, fontweight='bold')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_resource_usage(concurrency_list, cpu_list, ram_list, output_path):
    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.set_xlabel("Concurrency / Load", fontsize=11)
    ax1.set_ylabel("CPU Utilization (%)", color='tab:blue', fontsize=11)
    ax1.plot(concurrency_list, cpu_list, color='tab:blue', marker='o', linewidth=2, label="CPU %")
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel("Memory RSS (MB)", color='tab:red', fontsize=11)
    ax2.plot(concurrency_list, ram_list, color='tab:red', marker='s', linewidth=2, linestyle='--', label="RAM (MB)")
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title("Edge Node Resource Utilization Profile", fontsize=13, fontweight='bold')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_ablation_comparison(ablation_labels, p95_values, output_path):
    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.barh(ablation_labels, p95_values, color='#3498db')
    ax.set_title("Ablation Study: Impact on P95 System Latency", fontsize=13, fontweight='bold')
    ax.set_xlabel("P95 Pure System Latency (ms)", fontsize=11)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, f"{width:.2f} ms",
                ha='left', va='center', fontsize=10)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
