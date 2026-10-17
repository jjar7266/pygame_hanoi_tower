# Step 4: Animate Tower of Hanoi using a timer.
# This loads the move list from Step 1 and performs one move at a time.
# Each timer tick moves a single disk between rods and updates positions.
# Straight-line beginner logic. No clever tricks.

# Import modules
import pygame
import sys
from hanoi_logic import generate_hanoi_moves  # Step 1 logic

# Initialize Pygame
pygame.init()

# Create the display window
WIDTH  = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi - Step 4")

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
    (WIDTH * 3)  // 4
]
rod_y_top  = 150
rod_height = 350
rod_width  = 10

# Number of disks
NUM_DISKS = 5

# Rod structures
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
        "rod": "A",
        "x": 0,
        "y": 0
    }

    rod_A.append(disk)

# Recalculate x/y positions for all disks
def update_disk_positions():
    for rod_name, rod_list, rod_x in [
        ("A", rod_A, rod_x_positions[0]),
        ("B", rod_B, rod_x_positions[1]),
        ("C", rod_C, rod_x_positions[2])
    ]:
        for index, disk in enumerate(rod_list):
            disk["rod"] = rod_name
            disk["x"]   = rod_x - disk["width"] // 2
            disk["y"]   = (rod_y_top + rod_height) - (index + 1) * disk_height

update_disk_positions()

# Load move list from Step 1
moves = generate_hanoi_moves(NUM_DISKS)
move_index = 0

# Timer event for animation
MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 600)  # move every 600ms

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Perform one move per timer tick
        if event.type == MOVE_EVENT:
            if move_index < len(moves):
                disk_num, from_rod, to_rod = moves[move_index]

                # Select correct rod lists
                if from_rod == "A": source = rod_A
                elif from_rod == "B": source = rod_B
                else: source = rod_C

                if to_rod == "A": target = rod_A
                elif to_rod == "B": target = rod_B
                else: target = rod_C

                # Remove disk from source rod
                moving_disk = source.pop()

                # Add disk to target rod
                target.append(moving_disk)

                # Update positions
                update_disk_positions()

                move_index += 1

    # Draw background
    screen.fill(BG_COLOR)

    # Draw rods
    for rod_x in rod_x_positions:
        pygame.draw.rect(screen, ROD_COLOR, (rod_x - rod_width // 2, rod_y_top, rod_width, rod_height))

    # Draw disks
    for rod in (rod_A, rod_B, rod_C):
        for d in rod:
            pygame.draw.rect(screen, d["color"], (d["x"], d["y"], d["width"], d["height"]))

    pygame.display.flip()
    clock.tick(60)

    
