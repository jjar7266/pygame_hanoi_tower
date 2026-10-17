# OOP Step 1: Create Disk and Rod classes.
# This step only draws rods and disks using OOP.
# No animation, no moves, no buttons yet.

# Import modules
import pygame
import sys

# Initialize Pygame
pygame.init()

# Create the window display
WIDTH, HEIGHT = (900, 650)
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Tower of Hanoi - OOP Step 1")

# COLORS
BG_COLOR  = ("#1e1e1e")
ROD_COLOR = ("#c8c8c8")
DISK_COLORS = [
    ("#ff6464"),
    ("#ffb464"),
    ("#ffff64"),
    ("#b4ff64"),
    ("#64ffb4"),
    ("#64b4ff"),
    ("#b464ff"),
    ("#ff64b4")
]

# Disk settings
BASE_WIDTH  = 200
DISK_HEIGHT = 25

# Disk class
class Disk:
    # Each disk has width, height, color, rod reference, x/y position
    def __init__(self, width, color):
        self.width = width
        self.height = DISK_HEIGHT
        self.color = color
        self.x = 0
        self.y = 0
        self.rod = None

    # Draw the disk
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))


# Rod class
class Rod:
    # Each rod has a name, x position, and a list of disks
    def __init__(self, name, x_pos):
        self.name = name
        self.x_pos = x_pos
        self.disks = []

    # Add a disk to this rod
    def push_disk(self, disk):
        disk.rod = self
        self.disks.append(disk)
        self.update_positions()

    # Remove top disk
    def pop_disk(self):
        if self.disks:
            disk = self.disks.pop()
            self.update_positions()
            return disk
        return None

    # Recalculate x/y positions for all disks
    def update_positions(self):
        for index, disk in enumerate(self.disks):
            disk.x = self.x_pos - disk.width // 2
            disk.y = (150 + 350) - (index + 1) * DISK_HEIGHT

    # Draw the rod
    def draw(self, surface):
        pygame.draw.rect(surface, ROD_COLOR, (self.x_pos - 5, 150, 10, 350))


# Main App class
class App:
    def __init__(self):
        # Create rods
        self.rod_A = Rod("A", WIDTH // 4)
        self.rod_B = Rod("B", WIDTH // 2)
        self.rod_C = Rod("C", (WIDTH * 3) // 4)

        # Number of disks
        self.num_disks = 5

        # Build disks and place them on rod A
        for i in range(self.num_disks):
            width = BASE_WIDTH - (i * 20)
            color = DISK_COLORS[i]
            disk = Disk(width, color)
            self.rod_A.push_disk(disk)

        self.clock = pygame.time.Clock()

    # Draw everything
    def draw(self):
        screen.fill(BG_COLOR)

        # Draw rods
        self.rod_A.draw(screen)
        self.rod_B.draw(screen)
        self.rod_C.draw(screen)

        # Draw disks
        for rod in (self.rod_A, self.rod_B, self.rod_C):
            for disk in rod.disks:
                disk.draw(screen)

        pygame.display.flip()

    # Main loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw()
            self.clock.tick(60)


# Start the app
if __name__ == "__main__":
    app = App()
    app.run()

    

