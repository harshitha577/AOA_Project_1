import random
from collections import defaultdict

def generate_reads(genome, read_len, num_reads):
    """Generate random reads from a given genome string."""
    reads = []
    for _ in range(num_reads):
        start = random.randint(0, len(genome) - read_len)
        reads.append(genome[start:start+read_len])
    return reads


def build_debruijn_graph(reads, k):
    """Build a directed multigraph G = (V, E) from reads."""
    adj = defaultdict(list)
    indeg = defaultdict(int)
    outdeg = defaultdict(int)

    for read in reads:
        for i in range(len(read) - k):
            u = read[i:i+k]
            v = read[i+1:i+k+1]
            adj[u].append(v)
            outdeg[u] += 1
            indeg[v] += 1
            # ensure all nodes exist in dictionaries
            indeg[u] += 0
            outdeg[v] += 0
    return adj, indeg, outdeg
