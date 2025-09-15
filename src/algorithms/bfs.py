from queue import Queue
from math import inf


def bfs(G,s):
    n = len(G)
    Q = Queue()
    visited = [False] * n
    parent = [None] * n
    dist = [inf] * n

    dist[s] = 0
    visited[s] = True
    Q.put(s)

    while not Q.empty():
        u = Q.get()
        for v in G[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                dist[v] = dist[u] + 1
                Q.put(v)