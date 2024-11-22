import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import heapq

# Define grid size
GRID_SIZE = 100
NODE_SIZE = 10

# Define colors
WHITE = (1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0)
RED = (1.0, 0.0, 0.0)

# Define graph and costs
graph = {}
costs = {}

# Function to initialize OpenGL
def init():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b'Dijkstra Algorithm in OpenGL')

    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, 800, 0, 600)
    glClearColor(*WHITE)

# Function to draw grid
def draw_grid():
    glColor3f(*BLACK)
    glBegin(GL_LINES)
    for i in range(0, 800, GRID_SIZE):
        glVertex2i(i, 0)
        glVertex2i(i, 600)
        glVertex2i(0, i)
        glVertex2i(800, i)
    glEnd()

# Function to draw path
def draw_path(path):
    glColor3f(*RED)
    glLineWidth(3)
    glBegin(GL_LINE_STRIP)
    for node in path:
        x, y = node
        glVertex2i(x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2)
    glEnd()

# Function to calculate minimum cost path using Dijkstra's algorithm
def dijkstra(start, end):
    queue = [(0, start)]
    heapq.heapify(queue)
    visited = set()
    while queue:
        cost, node = heapq.heappop(queue)
        if node == end:
            break
        if node not in visited:
            visited.add(node)
            for neighbor, neighbor_cost in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + neighbor_cost, neighbor))
                    costs[neighbor] = cost + neighbor_cost

# Main function
def main():
    # Initialize graph
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            neighbors = []
            if i > 0:
                neighbors.append(((i - 1, j), 1))  # Left neighbor
            if i < GRID_SIZE - 1:
                neighbors.append(((i + 1, j), 1))  # Right neighbor
            if j > 0:
                neighbors.append(((i, j - 1), 1))  # Bottom neighbor
            if j < GRID_SIZE - 1:
                neighbors.append(((i, j + 1), 1))  # Top neighbor
            graph[(i, j)] = neighbors

    # Example start and end points
    start = (0, 0)
    end = (GRID_SIZE - 1, GRID_SIZE - 1)

    # Calculate minimum cost path using Dijkstra's algorithm
    dijkstra(start, end)

    # Get the minimum cost path
    path = [end]
    while path[-1] != start:
        min_neighbor = min(graph[path[-1]], key=lambda x: costs[x[0]])
        path.append(min_neighbor[0])
    path.reverse()

    # Initialize OpenGL
    init()

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        draw_path(path)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
