# OOP Step 7: Manual mode + auto mode separation.
# Adds:
#  - Manual rod-click mode (instant moves)
#  - Clean separation between AUTO and MANUAL
#  - Difficulty selector, restart, timer, move counter remain

# Import modules
import pygame
import sys
import time
from hanoi_logic import generate_hanoi_moves

# Initialize Pygame
pygame.init()

# Create the display window
WIDTH, HEIGHT = 1300, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi - OOP Step 7")

# COLORS (RGB tuples)
BG_COLOR   = ( 30,  30,  30)     # Charcoal
ROD_COLOR  = (200, 200, 200)     # Light Gray
BTN_COLOR  = ( 60,  60,  60)     # Onyx
BTN_HOVER  = (100, 100, 100)     # Medium Graw
TEXT_COLOR = (230, 230, 230)     # Whitesmoke

DISK_COLORS = [
    (255, 100, 100),   # Coral Red
    (255, 180, 100),   # Apricot
    (255, 255, 100),   # Lemon Yellow
    (180, 255, 100),   # Spring Green
    (100, 255, 180),   # Aquamarine Mint
    (100, 180, 255),   # Sky Blue
    (180, 100, 255),   # Lavender Purple
    (255, 100, 180)    # Rose Pink
]

BASE_WIDTH  = 200
DISK_HEIGHT = 25

# Vertical starting position of the rods and disks
ROD_TOP_Y = 200

# How high disks lift before sliding horizontally
LIFT_HEIGHT = ROD_TOP_Y - 50

font = pygame.font.SysFont("arial", 22)

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
            disk.y = (ROD_TOP_Y + 350) - (index + 1) * DISK_HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, ROD_COLOR, (self.x_pos - 5, ROD_TOP_Y, 10, 350))


# HanoiGame class
class HanoiGame:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.reset()

    def reset(self):
        self.rod_A = Rod("A", WIDTH // 4)
        self.rod_B = Rod("B", WIDTH // 2)
        self.rod_C = Rod("C", (WIDTH * 3) // 4)

        for i in range(self.num_disks):
            width = BASE_WIDTH - (i * 20)
            color = DISK_COLORS[i]
            disk  = Disk(width, color)
            self.rod_A.push_disk(disk)

        # AUTO mode solver moves
        self.moves = generate_hanoi_moves(self.num_disks)
        self.move_index = 0

        # Animation state
        self.animating  = False
        self.anim_disk  = None
        self.anim_phase = "lift"
        self.target_x   = 0
        self.target_y   = 0
        self.speed      = 4

        # Manual mode state
        self.manual_source = None

        self.start_time = time.time()

    def get_rod(self, name):
        if name == "A":
            return self.rod_A
        elif name == "B":
            return self.rod_B
        return self.rod_C

    # AUTO MODE animation
    def start_animation(self):
        if self.move_index >= len(self.moves):
            return

        disk_num, from_rod, to_rod = self.moves[self.move_index]
        source = self.get_rod(from_rod)
        target = self.get_rod(to_rod)

        self.anim_disk = source.pop_disk()
        if not self.anim_disk:
            return

        self.anim_phase = "lift"
        self.animating = True

        self.target_x = target.x_pos - self.anim_disk.width // 2
        self.target_y = (ROD_TOP_Y + 350) - (len(target.disks) + 1) * DISK_HEIGHT

    def update_animation(self):
        if not self.animating or not self.anim_disk:
            return

        if self.anim_phase == "lift":
            self.anim_disk.y -= self.speed
            if self.anim_disk.y <= LIFT_HEIGHT:
                self.anim_phase = "slide"

        elif self.anim_phase == "slide":
            if abs(self.anim_disk.x - self.target_x) > self.speed:
                if self.anim_disk.x < self.target_x:
                    self.anim_disk.x += self.speed
                else:
                    self.anim_disk.x -= self.speed
            else:
                self.anim_disk.x = self.target_x
                self.anim_phase = "drop"

        elif self.anim_phase == "drop":
            if self.anim_disk.y < self.target_y:
                self.anim_disk.y += self.speed
            else:
                target = self.get_rod(self.moves[self.move_index][2])
                target.push_disk(self.anim_disk)

                self.animating = False
                self.anim_disk = None
                self.move_index += 1

    # MANUAL MODE instant rod-click moves
    def manual_click(self, mx):
        # Detect rod by x position
        if abs(mx - self.rod_A.x_pos) < 80:
            rod = self.rod_A
        elif abs(mx - self.rod_B.x_pos) < 80:
            rod = self.rod_B
        elif abs(mx - self.rod_C.x_pos) < 80:
            rod = self.rod_C
        else:
            return

        # First click selects source rod
        if self.manual_source is None:
            if rod.disks:
                self.manual_source = rod
            return

        # Second click selects target rod
        if rod is not self.manual_source:

            # Pop the top disk from the source rod
            disk = self.manual_source.pop_disk()

            # Check size rule: cannot place larger disk on smaller disk
            if rod.disks and disk.width > rod.disks[-1].width:
                # Illegal move: do nothing, return disk to source rod
                self.manual_source.push_disk(disk)
            else:
                rod.push_disk(disk)

        self.manual_source = None

    def draw(self, surface):
        self.rod_A.draw(surface)
        self.rod_B.draw(surface)
        self.rod_C.draw(surface)

        for rod in (self.rod_A, self.rod_B, self.rod_C):
            for disk in rod.disks:
                disk.draw(surface)

        if self.anim_disk:
            self.anim_disk.draw(surface)


# Button class
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        color = BTN_COLOR
        if self.rect.collidepoint(mouse):
            color = BTN_HOVER

        pygame.draw.rect(surface, color, self.rect)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 8))

    def is_clicked(self, mx, my):
        return self.rect.collidepoint(mx, my)


# Main App class
class App:
    def __init__(self):
        self.game = HanoiGame(5)
        self.clock = pygame.time.Clock()

        self.buttons = [
            Button(50,  20, 120, 40, "Auto"),
            Button(180, 20, 120, 40, "Manual"),
            Button(310, 20, 120, 40, "Restart"),
            Button(440, 20, 120, 40, "Slow"),
            Button(570, 20, 120, 40, "Medium"),
            Button(700, 20, 120, 40, "Fast"),
            Button(830, 20, 60, 40, "3"),
            Button(900, 20, 60, 40, "4"),
            Button(970, 20, 60, 40, "5"),
            Button(1040, 20, 60, 40, "6"),
            Button(1110, 20, 60, 40, "7"),
            Button(1180, 20, 60, 40, "8")
        ]

        self.state = "AUTO"

    def draw(self):
        screen.fill(BG_COLOR)

        for btn in self.buttons:
            btn.draw(screen)

        self.game.draw(screen)

        moves_text = f"Moves: {self.game.move_index} / {len(self.game.moves)}"
        time_text = f"Time: {int(time.time() - self.game.start_time)}s"

        screen.blit(font.render(moves_text, True, TEXT_COLOR), (50, 80))
        screen.blit(font.render(time_text, True, TEXT_COLOR), (250, 80))

        pygame.display.flip()

    def handle_button_click(self, text):
        if text == "Auto":
            self.game.reset()
            self.state = "AUTO"

        elif text == "Manual":
            self.state = "MANUAL"

            # If an animation is in progress, safely cancel it
            if self.game.animating and self.game.anim_disk:
                # Return disk to its original rod
                source = self.game.get_rod(self.game.moves[self.game.move_index][1])
                source.push_disk(self.game.anim_disk)

            # Stop animation cleanly
            self.game.animating = False
            self.game.anim_disk = None

        elif text == "Restart":
            self.game.reset()

        elif text in ["3", "4", "5", "6", "7", "8"]:
            self.game = HanoiGame(int(text))

        elif text == "Slow":
            self.game.speed = 2

        elif text == "Medium":
            self.game.speed = 4

        elif text == "Fast":
            self.game.speed = 8

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    for btn in self.buttons:
                        if btn.is_clicked(mx, my):
                            self.handle_button_click(btn.text)

                    if self.state == "MANUAL":
                        self.game.manual_click(mx)

            if self.state == "AUTO":
                if not self.game.animating:
                    self.game.start_animation()
                self.game.update_animation()

            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    app = App()
    app.run()


