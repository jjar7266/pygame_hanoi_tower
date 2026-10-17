# Step 2: Minimal pygame window with rods and static disks.
# This draws three rods and a stack of disks on rod A.
# No animation yet. This is just the visual layout,

# Import modules
import pygame
import sys

# Initialize Pygame
pygame.init()

# Create the window display
WIDTH  = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi - Step 2")

# Colors
BG_COLOR  = ( 30,  30,  30)
ROD_COLOR = (200, 200, 200)
DISK_COLORS = [
    (255, 100, 100),
    (255, 180, 100),
    (255, 255, 100),
    (180, 255, 100),
    (100, 255, 180),
    (100, 180, 255),
    (180, 100, 255),
    (255, 100, 180)
]

# Rod positions
rod_x_positions = [
    WIDTH // 4,
    WIDTH // 2,
    (WIDTH * 3) // 4
]
rod_y_top  = 150
rod_height = 350
rod_width  = 10

# Number of disks (3-8)
NUM_DISKS = 5

# Build static disks for rod A
# Each disk is a dictionary with width, height, color, and position
disks = []
base_width  = 200
disk_height = 25

for i in range(NUM_DISKS):
    width = base_width - (i * 20)
    color = DISK_COLORS[i]
    x = rod_x_positions[0] - width // 2
    y = (rod_y_top + rod_height) - (i + 1) * disk_height
    disks.append({"width": width, "height": disk_height, "color": color, "x": x, "y": y })

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    screen.fill(BG_COLOR)

    # Draw rods
    for rod_x in rod_x_positions:
        pygame.draw.rect(screen, ROD_COLOR, (rod_x - rod_width // 2, rod_y_top, rod_width, rod_height))

    # Draw disks
    for d in disks:
        pygame.draw.rect(screen, d["color"], (d["x"], d["y"], d["width"], d["height"]))

    pygame.display.flip()
    clock.tick(60)

    
