# Step 3: Convert static disks into rod structures.
# We now have rod_A, rod_B, rod_C lists that hold disk dictionaries.
# A helper function update_disk_position() recalculates x/y positions
# based on which rod each disk is currently on.
# No animation yet. This prepares the data for Step 4.

# Import modules
import pygame
import sys

# Initialize Pygame
pygame.init()

# Create the display window
WIDTH  = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi - Step 3")

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

# Rod Structures
rod_A = []
rod_B = []
rod_C = []

# Build disks and place them on rod A
base_width  = 200
disk_height = 25

for i in range(NUM_DISKS):
    width = base_width - (i * 20)
    color = DISK_COLORS[i]

    disk = {
        "width": width,
        "height": disk_height,
        "color": color,
        "rod": "A",  # Starting rod
        "x": 0,
        "y": 0
    }

    rod_A.append(disk)

# This function recalculates x/y positions for all disks
def update_disk_positions():
    # For each rod, stack disks from bottom to top
    for rod_name, rod_list, rod_x in [
        ("A", rod_A, rod_x_positions[0]),
        ("B", rod_B, rod_x_positions[1]),
        ("C", rod_C, rod_x_positions[2])
    ]:
        for index, disk in enumerate(rod_list):
            disk["rod"] = rod_name
            disk["x"]   = rod_x - disk["width"] // 2
            disk["y"]   = (rod_y_top + rod_height) - (index + 1) * disk_height

# Initial positioning
update_disk_positions()

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

    # Draw disk from all rods
    for rod in (rod_A, rod_B, rod_C):
        for d in rod:
            pygame.draw.rect(screen, d["color"], (d["x"], d["y"], d["width"], d["height"]))

    pygame.display.flip()
    clock.tick(60)


