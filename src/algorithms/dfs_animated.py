from math import inf


def dfs_animated(graph,start_node_id):
    Q = []
    visited = {}
    parent = {}
    dist = {}

    for node_id in graph.nodes:
        visited[node_id] = False
        parent[node_id] = None
        dist[node_id] = inf

    dist[start_node_id] = 0
    visited[start_node_id] = True
    Q.append(start_node_id)

    while Q:
        u = Q.pop()

        #obecnie przetwarzany wierzchołek zmieniamy na kolor czerwony
        graph.nodes[u].color = (255,0,0)
        yield {
            "message": f"Przetwarzam węzeł {u}",
            "algorithm": "dfs",
            "queue": Q.copy(),  # Aktualna kolejka
            "visited": visited.copy(),
            "parent": parent.copy(),
            "dist": dist.copy(),
            "current_node": u
        }

        neighbors = graph.get_neighbors(u)
        for neighbor_node in neighbors:
            v = neighbor_node.id
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                dist[v] = dist[u] + 1
                Q.append(v)

                #węzły w kolejce zmieniamy na kolor zółty
                graph.nodes[v].color = (255,255,0) 
                yield {
                    "message": f"Dodaję węzeł {v} do stosu",
                    "algorithm": "dfs",
                    "queue": Q.copy(),
                    "visited": visited.copy(),
                    "parent": parent.copy(),
                    "dist": dist.copy(),
                    "current_node": u
                }

        #przetworzony juz wierzchołek ustawiamy na kolor zielony
        graph.nodes[u].color = (0,255,0)
        yield {
            "message": f"Węzeł {u} przetworzony",
            "algorithm": "dfs",
            "queue": Q.copy(),
            "visited": visited.copy(),
            "parent": parent.copy(),
            "dist": dist.copy(),
            "current_node": None
        }

    return visited, parent, dist