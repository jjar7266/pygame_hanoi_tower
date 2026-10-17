# OOP Step 2: Add HanioGame class.
# This step adds the puzzle logic:
#  - rods stored inside HanoiGame
#  - move list from generate_hanoi_moves()
#  - move index
#  - do_next_move()
#  - do_back_move()
# No buttons, no animation yet. Just logic.

# Import modules
import pygame
import sys
from hanoi_logic import generate_hanoi_moves

# Initialize Pygame
pygame.init()

# Create the display window
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi - OOP Step 2")

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

BASE_WIDTH  = 200
DISK_HEIGHT = 25


# Disk class
class Disk:
    def __init__(self, width, color):
        self.width = width
        self.height = DISK_HEIGHT
        self.color = color
        self.x = 0
        self.y = 0
        self.rod = None

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))


# Rod class
class Rod:
    def __init__(self, name, x_pos):
        self.name = name
        self.x_pos = x_pos
        self.disks = []

    def push_disk(self, disk):
        disk.rod = self
        self.disks.append(disk)
        self.update_positions()

    def pop_disk(self):
        if self.disks:
            disk = self.disks.pop()
            self.update_positions()
            return disk
        return None

    def update_positions(self):
        for index, disk in enumerate(self.disks):
            disk.x = self.x_pos - disk.width // 2
            disk.y = (150 + 350) - (index + 1) * DISK_HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, ROD_COLOR, (self.x_pos - 5, 150, 10, 350))


# HanoiGame class
class HanoiGame:
    def __init__(self, num_disks):
        self.num_disks = num_disks

        # Create rods
        self.rod_A = Rod("A", WIDTH // 4)
        self.rod_B = Rod("B", WIDTH // 2)
        self.rod_C = Rod("C", (WIDTH * 3) // 4)

        # Build disks on rod A
        for i in range(self.num_disks):
            width = BASE_WIDTH - (i * 20)
            color = DISK_COLORS[i]
            disk = Disk(width, color)
            self.rod_A.push_disk(disk)

        # Load move list
        self.moves = generate_hanoi_moves(self.num_disks)
        self.move_index = 0

    # Move forward one step
    def do_next_move(self):
        if self.move_index >= len(self.moves):
            return

        disk_num, from_rod, to_rod = self.moves[self.move_index]

        source = self.get_rod(from_rod)
        target = self.get_rod(to_rod)

        disk = source.pop_disk()
        target.push_disk(disk)

        self.move_index += 1

    # Undo one step
    def do_back_move(self):
        if self.move_index <= 0:
            return

        self.move_index -= 1
        disk_num, from_rod, to_rod = self.moves[self.move_index]

        # Reverse direction
        source = self.get_rod(to_rod)
        target = self.get_rod(from_rod)

        disk = source.pop_disk()
        target.push_disk(disk)

    # Helper: get rod by name
    def get_rod(self, name):
        if name == "A":
            return self.rod_A
        elif name == "B":
            return self.rod_B
        return self.rod_C

    # Draw everything
    def draw(self, surface):
        self.rod_A.draw(surface)
        self.rod_B.draw(surface)
        self.rod_C.draw(surface)

        for rod in (self.rod_A, self.rod_B, self.rod_C):
            for disk in rod.disks:
                disk.draw(surface)


# Main App class
class App:
    def __init__(self):
        self.game = HanoiGame(5)
        self.clock = pygame.time.Clock()

    def draw(self):
        screen.fill(BG_COLOR)
        self.game.draw(screen)
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # TEMPORARY: press right arrow to step forward
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.game.do_next_move()
                    if event.key == pygame.K_LEFT:
                        self.game.do_back_move()

            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    app = App()
    app.run()


