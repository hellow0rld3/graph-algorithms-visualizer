import pygame
import sys
import math

from graph import Graph
from algorithms.bfs_animated import bfs_animated
from algorithms.dfs_animated import dfs_animated

def find_node_at_position(graph, x, y):
    """Znajdź węzeł na danej pozycji (sprawdza kolizję z okręgiem)"""
    for node in graph.nodes.values():
        distance = math.sqrt((x - node.x)**2 + (y - node.y)**2)
        if distance <= node.radius:
            return node
    return None

def draw_algorithm_state(screen, data, font):
    """Rysuj aktualny stan algorytmu (BFS lub DFS) po prawej stronie"""
    if data is None:
        return
    
    x_start = 950
    y_start = 50
    line_height = 25

    is_dfs = data.get("algorithm") == "dfs"
    
    # Tytuł
    title_text = "Stan DFS:" if is_dfs else "Stan BFS:"
    title = font.render(title_text, True, (0, 0, 0))
    screen.blit(title, (x_start, y_start))
    y = y_start + 40

    # Kolejka/Stos
    queue_label = "Stos: " if is_dfs else "Kolejka: "
    queue_text = font.render(queue_label + str(data["queue"]), True, (0, 0, 0))
    screen.blit(queue_text, (x_start, y))
    y += line_height

    # Odwiedzone węzły
    visited_nodes = [k for k, v in data["visited"].items() if v]
    visited_text = font.render("Odwiedzone: " + str(visited_nodes), True, (0, 0, 0))
    screen.blit(visited_text, (x_start, y))
    y += line_height

    # Aktualnie przetwarzany
    if data["current_node"] is not None:
        current_text = font.render(f"Aktualny: {data['current_node']}", True, (255, 0, 0))
        screen.blit(current_text, (x_start, y))
    y += line_height * 2

    # Odległości tylko dla BFS
    if not is_dfs:
        dist_text = font.render("Odległości:", True, (0, 0, 0))
        screen.blit(dist_text, (x_start, y))
        y += line_height

        for node_id in visited_nodes:
            if data["dist"][node_id] != float('inf'):
                text = font.render(f"  {node_id}: {data['dist'][node_id]}", True, (0, 0, 0))
                screen.blit(text, (x_start, y))
                y += line_height

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

    dragging = False
    drag_start_node = None
    bfs_gen = None
    dfs_gen = None
    current_bfs_data = None

    graph = Graph()

    while running:

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_node = find_node_at_position(graph, mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    clicked_node = find_node_at_position(graph,x,y)
                    #zaczynamy przeciąganie jeśli zaczynamy klikać w istniejący węzeł
                    if clicked_node is not None:
                        dragging = True
                        drag_start_node = clicked_node
                    #dodajemy węzeł jezeli kliknęliśmy w puste miejsce
                    else:
                        graph.add_node(x,y)
                
                #Usuwanie węzła
                if event.button == 3:
                    x, y = event.pos
                    clicked_node = find_node_at_position(graph, x, y)
                    if clicked_node is not None:
                        # Usuń wszystkie krawędzie połączone z tym węzłem
                        graph.edges = [edge for edge in graph.edges 
                                     if edge.node1.id != clicked_node.id and 
                                        edge.node2.id != clicked_node.id]
                        del graph.nodes[clicked_node.id]

            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                x, y = event.pos
                drag_end_node = find_node_at_position(graph,x,y)
                if drag_end_node is not None and drag_end_node != drag_start_node:
                    graph.add_edge(drag_start_node.id, drag_end_node.id)

                dragging = False
                drag_start_node = None
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(graph.nodes) > 0:

                        for node in graph.nodes.values():
                            node.color = (100, 100, 100)

                        start_id = list(graph.nodes.keys())[0]
                        bfs_gen = bfs_animated(graph,start_id)

                
                elif event.key == pygame.K_RIGHT:
                    if bfs_gen is not None:
                        try:
                            data = next(bfs_gen)
                            print(data["message"])

                            current_bfs_data = data
                        except StopIteration:
                            print("BFS zakończony")
                            bfs_gen = None
                            current_bfs_data = None
                    
                    elif dfs_gen is not None:
                        try:
                            data = next(dfs_gen)
                            print(data["message"])
                            current_bfs_data = data  # Używamy tej samej zmiennej do wyświetlania
                        except StopIteration:
                            print("DFS zakończony!")
                            dfs_gen = None
                            current_bfs_data = None

                elif event.key == pygame.K_LSHIFT:  # Lewy Shift
                    if len(graph.nodes) > 0:
                        # Resetuj kolory
                        for node in graph.nodes.values():
                            node.color = (100, 100, 100)
                        
                        start_id = list(graph.nodes.keys())[0]
                        dfs_gen = dfs_animated(graph, start_id)
                        graph.nodes[start_id].color = (255, 255, 0)

        screen.fill(WHITE)
        
        #Rysujemy krawędzie, aby były "pod" węzłami

        for edge in graph.edges:
            pygame.draw.line(screen, edge.color, (edge.node1.x, edge.node1.y), 
                             (edge.node2.x, edge.node2.y), 3)
        

        # Narysuj tymczasową linię od węzła startowego do kursora
        if dragging and drag_start_node is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255, 0, 0), 
                            (drag_start_node.x, drag_start_node.y), 
                            (mouse_x, mouse_y), 2)
            
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

        if current_bfs_data:
            instruction_font = pygame.font.Font(None, 20) 
            draw_algorithm_state(screen, current_bfs_data, instruction_font)  
    
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
