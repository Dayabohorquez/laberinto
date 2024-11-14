import pygame
import heapq
import sys

WIDTH, HEIGHT = 500, 500
ROWS, COLS = 20, 20
GRID_SIZE = WIDTH // COLS
BLACK, WHITE, RED, GREEN, BLUE, YELLOW = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laberinto con IA (A*)")

font = pygame.font.Font(None, 36)

class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.color = WHITE
        self.neighbors = []
        self.g_score = float('inf')

    def __lt__(self, other):
        return self.g_score < other.g_score
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.col * GRID_SIZE, self.row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BLACK, (self.col * GRID_SIZE, self.row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def add_neighbors(self, grid):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c].color != BLACK:
                self.neighbors.append(grid[r][c])

def astar(start, end):
    open_set = [(0, start)]
    came_from, g_score = {start: None}, {start: 0}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            return reconstruct_path(came_from, end)
        for neighbor in current.neighbors:
            if neighbor.color == BLACK:
                continue
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score, neighbor))
                if neighbor.color != GREEN and neighbor.color != RED:
                    neighbor.color = BLUE
        draw()
    return []


def heuristic(node1, node2):
    return abs(node1.row - node2.row) + abs(node1.col - node2.col)

def reconstruct_path(came_from, current):
    path = []
    while current:
        path.append(current)
        current = came_from[current]
    return path

def draw():
    screen.fill(BLACK)
    for row in grid:
        for node in row:
            node.draw()
    pygame.display.update()

grid = [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]
for row in grid:
    for node in row:
        node.add_neighbors(grid)

start, end = grid[0][0], grid[ROWS-1][COLS-1]
start.color, end.color = GREEN, RED

running, solving = True, False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row, col = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
            if 0 <= row < ROWS and 0 <= col < COLS:
                node = grid[row][col]
                if node != start and node != end:
                    node.color = BLACK
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                solving = True

    if solving:
        solution_path = astar(start, end)
        if solution_path:
            for node in solution_path:
                node.color = YELLOW
            draw()
            text = font.render("¡Labirinto completado!", True, GREEN)
        else:
            text = font.render("Sin solución", True, RED)
        screen.blit(text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        solving = False

    draw()
pygame.quit()
