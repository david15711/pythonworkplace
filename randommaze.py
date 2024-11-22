import pygame
from pygame.locals import *
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Maze parameters
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 40
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random 2D Maze with DFS")

# Function to generate random maze
def generate_maze():
    maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.2:  # Adjust the probability as needed
                maze[i][j] = 1
                # Check neighbors
                if i>1 and j>1 and i<ROWS-1 and j<COLS-1:
                    if maze[i-1][j] == 1 and maze[i+1][j] == 1 and maze[i][j-1] == 1 and maze[i][j+1] == 1:
                        maze[i][j] = 1  # If all neighbors are walls, make the cell a wall
    maze[0][0] = 0
    return maze

# Function to draw maze
def draw_maze(maze):
    for i in range(ROWS):
        for j in range(COLS):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, WHITE, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 2:
                pygame.draw.rect(screen, BLUE, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Depth-first search algorithm
def dfs(maze, i, j, direction):
    if i < 0 or i >= ROWS or j < 0 or j >= COLS or maze[i][j] == 1 or maze[i][j] == 2:
        return
    maze[i][j] = 2
    draw_maze(maze)
    pygame.display.flip()
    pygame.time.delay(50)  # Adjust delay as needed
    if direction == 0:
        dfs(maze, i, j-1, (direction + 1) % 4)
        dfs(maze, i-1, j, direction)
        dfs(maze, i, j+1, (direction + 3) % 4)
        dfs(maze, i+1, j, (direction + 2) % 4)
    if direction == 1:
        dfs(maze, i+1, j, (direction + 1) % 4)
        dfs(maze, i, j-1, direction)
        dfs(maze, i-1, j, (direction + 3) % 4)
        dfs(maze, i, j+1, (direction + 2) % 4)
    if direction == 2:
        dfs(maze, i, j+1, (direction + 1) % 4)
        dfs(maze, i+1, j, direction)
        dfs(maze, i, j-1, (direction + 3) % 4)
        dfs(maze, i-1, j, (direction + 2) % 4)
    if direction == 3:
        dfs(maze, i-1, j, (direction + 1) % 4)
        dfs(maze, i, j+1, direction)
        dfs(maze, i+1, j, (direction + 3) % 4)
        dfs(maze, i, j-1, (direction + 2) % 4)

# Main function
def main():
    maze = generate_maze()
    draw_maze(maze)
    pygame.display.flip()
    dfs(maze, 0, 0, 0)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
