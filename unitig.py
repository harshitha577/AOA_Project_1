def find_unitigs(adj, indeg, outdeg):
    """
    Greedy extraction of maximal unitigs from de Bruijn graph.
    Returns: list of paths (each path = list of nodes)
    """
    visited_edges = set()
    unitigs = []

    # Identify anchors
    anchors = [v for v in adj.keys()
               if indeg[v] != 1 or outdeg[v] != 1 or
                  (indeg[v] == 0 and outdeg[v] == 0)]

    # Greedy forward traversal
    for v in anchors:
        for w in adj[v]:
            edge = (v, w)
            if edge in visited_edges:
                continue

            path = [v]
            visited_edges.add(edge)
            u = w
            while indeg[u] == 1 and outdeg[u] == 1:
                path.append(u)
                next_w = adj[u][0]
                visited_edges.add((u, next_w))
                u = next_w

            path.append(u)
            unitigs.append(path)
    return unitigs
