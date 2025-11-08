# ==============================================================
# Divide & Conquer vs Brute Force Comparison for Cardiac Stress Detection
# ==============================================================
# Author: [Your Name]
# Description:
#   - Simulates cardiac stress ECG data.
#   - Compares Divide & Conquer (O(n log n)) and Brute Force (O(n^2)) algorithms.
#   - Measures runtime and visualizes scaling behavior.
# ==============================================================

import numpy as np
import time
import matplotlib.pyplot as plt
import math
import random

# --------------------------------------------------------------
# 1️⃣ Synthetic ECG-like Stress Data Generation
# --------------------------------------------------------------
def generate_stress_data(n, stress_ratio=0.1):
    """
    Generate synthetic ECG stress scores of length n.
    Positive = stress, Negative = recovery.
    """
    data = np.random.normal(-1.5, 1.5, n)
    bursts = max(1, int(stress_ratio * n))
    for _ in range(bursts):
        start = random.randint(0, n - 50)
        end = min(n, start + random.randint(10, 200))
        data[start:end] += np.random.uniform(3, 8)
    return data

# --------------------------------------------------------------
# 2️⃣ Brute Force Algorithm (O(n^2))
# --------------------------------------------------------------
def brute_force_max_subarray(arr):
    n = len(arr)
    max_sum = -float('inf')
    left = right = 0
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum > max_sum:
                max_sum = current_sum
                left, right = i, j
    return max_sum, left, right

# --------------------------------------------------------------
# 3️⃣ Divide and Conquer Algorithm (O(n log n))
# --------------------------------------------------------------
def max_crossing_sum(arr, low, mid, high):
    left_sum = -float('inf')
    total = 0
    max_left = mid
    for i in range(mid, low - 1, -1):
        total += arr[i]
        if total > left_sum:
            left_sum = total
            max_left = i

    right_sum = -float('inf')
    total = 0
    max_right = mid
    for j in range(mid + 1, high + 1):
        total += arr[j]
        if total > right_sum:
            right_sum = total
            max_right = j

    return left_sum + right_sum, max_left, max_right

def divide_and_conquer(arr, low, high):
    if low == high:
        return arr[low], low, high
    mid = (low + high) // 2
    left_sum, left_low, left_high = divide_and_conquer(arr, low, mid)
    right_sum, right_low, right_high = divide_and_conquer(arr, mid + 1, high)
    cross_sum, cross_low, cross_high = max_crossing_sum(arr, low, mid, high)
    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_sum, left_low, left_high
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return right_sum, right_low, right_high
    else:
        return cross_sum, cross_low, cross_high

# --------------------------------------------------------------
# 4️⃣ Experimental Benchmarking
# --------------------------------------------------------------
def benchmark_algorithms():
    input_sizes = [100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    times_brute = []
    times_dc = []

    for n in input_sizes:
        data = generate_stress_data(n)
        print(f"Running for n = {n}...")

        # Brute Force Timing
        if n <= 5000:  # Avoid long runtimes for very large n
            start = time.time()
            brute_force_max_subarray(data)
            end = time.time()
            times_brute.append(end - start)
        else:
            times_brute.append(np.nan)  # mark as not feasible

        # Divide and Conquer Timing
        start = time.time()
        divide_and_conquer(data, 0, len(data) - 1)
        end = time.time()
        times_dc.append(end - start)

    return input_sizes, times_brute, times_dc

# --------------------------------------------------------------
# 5️⃣ Visualization
# --------------------------------------------------------------
def plot_results(input_sizes, times_brute, times_dc):
    plt.figure(figsize=(8,5))
    plt.plot(input_sizes, times_dc, 'o-', color='blue', label='Divide & Conquer (O(n log n))')
    plt.plot(input_sizes, times_brute, 's--', color='red', label='Brute Force (O(n²))')
    plt.xlabel("Input Size (n)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime Comparison: Divide & Conquer vs Brute Force")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("dc_runtime_comparison.png", dpi=300)
    plt.show()

    # Log-Log Plot
    plt.figure(figsize=(8,5))
    valid_idx = [i for i, t in enumerate(times_brute) if not math.isnan(t)]
    plt.loglog(input_sizes, times_dc, 'o-', label='Divide & Conquer (O(n log n))', color='blue')
    plt.loglog([input_sizes[i] for i in valid_idx], [times_brute[i] for i in valid_idx],
               's--', label='Brute Force (O(n²))', color='red')
    plt.xlabel("Input Size (n) [log scale]")
    plt.ylabel("Runtime (seconds) [log scale]")
    plt.title("Log–Log Plot: Empirical Verification of Time Complexity")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("dc_loglog_plot.png", dpi=300)
    plt.show()

# --------------------------------------------------------------
# 6️⃣ Main Execution
# --------------------------------------------------------------
if __name__ == "__main__":
    input_sizes, times_brute, times_dc = benchmark_algorithms()
    plot_results(input_sizes, times_brute, times_dc)