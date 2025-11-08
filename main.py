import time
import matplotlib.pyplot as plt
from debruijn import generate_reads, build_debruijn_graph
from unitig import find_unitigs
import numpy as np
import os

def simulate_and_measure(genome_len=20000, read_len=50, k=21, sizes=[500, 1000, 2000, 4000, 8000]):
    """Run experiments for various numbers of reads and measure runtime."""
    genome = ''.join(__import__('random').choices('ACGT', k=genome_len))
    runtimes = []
    edges = []

    for num_reads in sizes:
        reads = generate_reads(genome, read_len, num_reads)
        adj, indeg, outdeg = build_debruijn_graph(reads, k)
        E = sum(len(vs) for vs in adj.values())
        edges.append(E)

        start = time.time()
        find_unitigs(adj, indeg, outdeg)
        end = time.time()

        runtime = end - start
        runtimes.append(runtime)
        print(f"{num_reads} reads → {E} edges → time = {runtime:.5f}s")

    return edges, runtimes


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    edges, runtimes = simulate_and_measure()

    # Convert to NumPy arrays for convenience
    edges = np.array(edges)
    runtimes = np.array(runtimes)

    # ---------- Plot 1: Runtime vs |E| ----------
    plt.figure(figsize=(7,5))
    plt.plot(edges, runtimes, 'o-', lw=2)
    plt.xlabel("Number of edges |E|", fontsize=12)
    plt.ylabel("Runtime (seconds)", fontsize=12)
    plt.title("Greedy Unitig Extraction Runtime (O(|E|))", fontsize=13)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/runtime_vs_edges.png")

    # ---------- Plot 2: Runtime per edge vs |E| ----------
    runtime_per_edge = runtimes / edges
    plt.figure(figsize=(7,5))
    plt.plot(edges, runtime_per_edge, 's--', lw=2, color='orange')
    plt.xlabel("Number of edges |E|", fontsize=12)
    plt.ylabel("Runtime per edge (seconds / edge)", fontsize=12)
    plt.title("Runtime per Edge vs |E| (Expected Constant for O(|E|))", fontsize=13)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/runtime_per_edge_vs_edges.png")

    plt.show()

    # Optional: print average runtime per edge
    avg = np.mean(runtime_per_edge)
    print(f"\nAverage runtime per edge ≈ {avg:.2e} seconds/edge (should stay roughly constant).")
