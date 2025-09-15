from queue import Queue
from math import inf


def bfs(graph,start_node_id):
    Q = Queue()
    visited = {}
    parent = {}
    dist = {}

    for node_id in graph.nodes:
        visited[node_id] = False
        parent[node_id] = None
        dist[node_id] = inf

    dist[start_node_id] = 0
    visited[start_node_id] = True
    Q.put(start_node_id)

    while not Q.empty():
        u = Q.get()
        neighbors = graph.get_neighbors(u)
        for neighbor_node in neighbors:
            v = neighbor_node.id
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                dist[v] = dist[u] + 1
                Q.put(v)

    return visited, parent, dist