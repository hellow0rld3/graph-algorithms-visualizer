import pygame
import sys
import math

from graph import Graph

def find_node_at_position(graph, x, y):
    """Znajdź węzeł na danej pozycji (sprawdza kolizję z okręgiem)"""
    for node in graph.nodes.values():
        distance = math.sqrt((x - node.x)**2 + (y - node.y)**2)
        if distance <= node.radius:
            return node
    return None

def main():
    pygame.init()

    #window setup
    WIDTH, HEIGHT = 1200, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Graph Algorithms Visualizer")

    WHITE = (255,255,255)
    BLACK = (0,0,0)
    GRAY = (100, 100, 100)
    RED = (255, 100, 100)
    BLUE = (100, 100, 255)

    clock = pygame.time.Clock()
    running = True
    hovered_node = None

    graph = Graph()

    while running:

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_node = find_node_at_position(graph, mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    graph.add_node(x,y)
                
                if event.button == 3:
                    x, y = event.pos
                    clicked_node = find_node_at_position(graph, x, y)
                    if clicked_node is not None:
                        # Usuń wszystkie krawędzie połączone z tym węzłem
                        graph.edges = [edge for edge in graph.edges 
                                     if edge.node1.id != clicked_node.id and 
                                        edge.node2.id != clicked_node.id]
                        del graph.nodes[clicked_node.id]


        screen.fill(WHITE)
        
        #Rysujemy krawędzie, aby były "pod" węzłami

        for edge in graph.edges:
            pygame.draw.line(screen, edge.color, (edge.node1.x, edge.node1.y), 
                             (edge.node2.x, edge.node2.y), 3)
            
        #Teraz węzły

        for node in graph.nodes.values():
            if node == hovered_node:
                color = BLUE
            else:
                color = node.color

            #rysujemy węzeł
            pygame.draw.circle(screen, color, (node.x, node.y), node.radius)

            #rysujemy obramowanie węzłów
            pygame.draw.circle(screen, BLACK, (node.x, node.y), node.radius, 2)

            #id węzłów
            font = pygame.font.Font(None,24)
            text = font.render(str(node.id), True, WHITE)
            text_rect = text.get_rect(center = (node.x, node.y))
            screen.blit(text, text_rect)

        #Informacje na ekranie
        info_font = pygame.font.Font(None, 36)
        info_text = f"Węzły: {len(graph.nodes)} | Krawędzie: {len(graph.edges)}"
        info_surface = info_font.render(info_text, True, BLACK)
        screen.blit(info_surface, (10, 10))


    
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
