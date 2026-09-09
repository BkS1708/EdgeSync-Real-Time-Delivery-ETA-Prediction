import math
import csv
import json
import os

def calculate_stats(numbers):
    if not numbers:
        return {
            "count": 0, "min": 0.0, "max": 0.0, "mean": 0.0,
            "median": 0.0, "stddev": 0.0, "p50": 0.0, "p90": 0.0,
            "p95": 0.0, "p99": 0.0, "ci_95_low": 0.0, "ci_95_high": 0.0
        }

    sorted_nums = sorted(numbers)
    count = len(sorted_nums)
    mean = sum(sorted_nums) / count

    variance = sum((x - mean) ** 2 for x in sorted_nums) / max(1, count - 1)
    stddev = math.sqrt(variance)

    def percentile(p):
        idx = int(math.ceil((p / 100.0) * count)) - 1
        idx = max(0, min(count - 1, idx))
        return sorted_nums[idx]

    p50 = percentile(50)
    p90 = percentile(90)
    p95 = percentile(95)
    p99 = percentile(99)

    margin = 1.96 * (stddev / math.sqrt(count)) if count > 1 else 0.0

    return {
        "count": count,
        "min": round(sorted_nums[0], 3),
        "max": round(sorted_nums[-1], 3),
        "mean": round(mean, 3),
        "median": round(p50, 3),
        "stddev": round(stddev, 3),
        "p50": round(p50, 3),
        "p90": round(p90, 3),
        "p95": round(p95, 3),
        "p99": round(p99, 3),
        "ci_95_low": round(mean - margin, 3),
        "ci_95_high": round(mean + margin, 3)
    }

def calculate_paired_ttest(sample_a, sample_b):
    """Calculates paired t-statistic and approximate two-tailed p-value for matched requests."""
    if not sample_a or not sample_b or len(sample_a) != len(sample_b) or len(sample_a) < 2:
        return {"t_stat": 0.0, "p_val": 1.0, "significant": False}

    diffs = [a - b for a, b in zip(sample_a, sample_b)]
    n = len(diffs)
    mean_diff = sum(diffs) / n
    var_diff = sum((d - mean_diff) ** 2 for d in diffs) / (n - 1)
    se_diff = math.sqrt(var_diff / n) if var_diff > 0 else 0.00001

    t_stat = mean_diff / se_diff
    # Approximation of normal / t distribution CDF for large N (N >= 30)
    abs_t = abs(t_stat)
    p_val = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs_t / math.sqrt(2.0))))

    return {
        "t_stat": round(t_stat, 4),
        "p_val": round(p_val, 6),
        "mean_diff": round(mean_diff, 4),
        "significant": p_val < 0.05
    }

def generate_markdown_table(headers, rows):
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        lines.append("| " + " | ".join(str(cell) for cell in r) + " |")
    return "\n".join(lines)
