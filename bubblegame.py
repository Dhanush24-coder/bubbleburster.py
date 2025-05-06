import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Shooter Game")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

# Colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 150, 255), (255, 255, 0), (255, 105, 180)]
BLACK = (0, 0, 0)

# Bubble settings
BUBBLE_RADIUS = 20
SPEED = 10
ROWS = 6
COLS = WIDTH // (BUBBLE_RADIUS * 2)

# Create grid for bubbles
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Bubble class
class Bubble:
    def __init__(self, x, y, color, moving=False, angle=0):
        self.x = x
        self.y = y
        self.color = color
        self.moving = moving
        self.angle = angle

    def move(self):
        self.x += SPEED * math.cos(self.angle)
        self.y += SPEED * math.sin(self.angle)

        if self.x - BUBBLE_RADIUS <= 0 or self.x + BUBBLE_RADIUS >= WIDTH:
            self.angle = math.pi - self.angle

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BUBBLE_RADIUS)

# Add some initial bubbles to the grid
def add_initial_bubbles():
    for row in range(3):  # Start with 3 rows of random bubbles
        for col in range(COLS):
            x = col * BUBBLE_RADIUS * 2 + BUBBLE_RADIUS
            y = row * BUBBLE_RADIUS * 2 + BUBBLE_RADIUS
            grid[row][col] = Bubble(x, y, random.choice(COLORS))

def get_grid_pos(x, y):
    col = x // (BUBBLE_RADIUS * 2)
    row = y // (BUBBLE_RADIUS * 2)
    return int(row), int(col)

# Check for 3 or more same-color bubbles
def check_matching(row, col, color, visited=None):
    if visited is None:
        visited = set()
    if (row < 0 or row >= ROWS or col < 0 or col >= COLS):
        return []
    if grid[row][col] is None or grid[row][col].color != color or (row, col) in visited:
        return []
    
    visited.add((row, col))
    matches = [(row, col)]
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        matches += check_matching(row+dr, col+dc, color, visited)
    return matches

# Main game variables
current_bubble = Bubble(WIDTH // 2, HEIGHT - 50, random.choice(COLORS), moving=False)
add_initial_bubbles()

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot bubble on click
        if event.type == pygame.MOUSEBUTTONDOWN and not current_bubble.moving:
            mx, my = pygame.mouse.get_pos()
            dx = mx - current_bubble.x
            dy = my - current_bubble.y
            angle = math.atan2(dy, dx)
            current_bubble.angle = angle
            current_bubble.moving = True

    # Move and check collisions
    if current_bubble.moving:
        current_bubble.move()
        row, col = get_grid_pos(current_bubble.x, current_bubble.y)
        if row < 0 or row >= ROWS or col < 0 or col >= COLS or grid[row][col] is not None or current_bubble.y <= 60:
            # Stick to grid
            r, c = get_grid_pos(current_bubble.x, current_bubble.y)
            r = max(0, min(ROWS - 1, r))
            c = max(0, min(COLS - 1, c))
            x = c * BUBBLE_RADIUS * 2 + BUBBLE_RADIUS
            y = r * BUBBLE_RADIUS * 2 + BUBBLE_RADIUS
            current_bubble.x, current_bubble.y = x, y
            grid[r][c] = current_bubble

            # Check for popping
            matches = check_matching(r, c, current_bubble.color)
            if len(matches) >= 3:
                for mr, mc in matches:
                    grid[mr][mc] = None

            # New bubble
            current_bubble = Bubble(WIDTH // 2, HEIGHT - 50, random.choice(COLORS), moving=False)

    # Draw grid
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col]:
                grid[row][col].draw()

    # Draw current bubble
    current_bubble.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
