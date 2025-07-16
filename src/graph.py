"""
Graph Data Structure
"""

class Node:
    def __init__(self, x, y, node_id):
        self.x = x
        self.y = y
        self.id = node_id
        self.color = (100,100,100)
        self.radius = 20

class Edge:
    def __init__(self, node1, node2, weight=1):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.color = (0,0,0)

class Graph:
    #Main graph class
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.next_id = 0

    def add_node(self,x,y):
        node = Node(x, y, self.next_id)
        self.nodes[self.next_id] = node
        self.next_id += 1
        return node
    
    def add_edge(self, node1_id, node2_id, weight=1):
        if node1_id and node2_id in self.nodes:
            node1 = self.nodes[node1_id]
            node2 = self.nodes[node2_id]
            edge = Edge(node1, node2, weight)
            self.edges.append(edge)
            return edge
        return None
    
    def get_neighbors(self, node_id):
        neighbors = []
        for edge in self.edges:
            if edge.node1.id == node_id:
                neighbors.append(edge.node2)
            
            #For undirected graphs
            elif edge.node2.id == node_id:
                neighbors.append(edge.node1)
                
        return neighbors