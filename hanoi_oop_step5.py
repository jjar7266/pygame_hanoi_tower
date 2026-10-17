# OOP Step 5: Smooth animation + speed control.
# Adds:
#  - Lift, slide, drop animation
#  - Adjustable speed (Slow, Medium, Fast)
#  - Clean OOP movement system

# Import modules
import pygame
import sys
from hanoi_logic import generate_hanoi_moves

# Initialize Pygame
pygame.init()

# Create the display window
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi - OOP Step 5")

# COLORS (RGB tuples)
BG_COLOR   = (30, 30, 30)
ROD_COLOR  = (200, 200, 200)
BTN_COLOR  = (60, 60, 60)
BTN_HOVER  = (100, 100, 100)
TEXT_COLOR = (230, 230, 230)

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

BASE_WIDTH  = 200
DISK_HEIGHT = 25

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
            disk.y = (150 + 350) - (index + 1) * DISK_HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, ROD_COLOR, (self.x_pos - 5, 150, 10, 350))


# HanoiGame class
class HanoiGame:
    def __init__(self, num_disks):
        self.num_disks = num_disks

        self.rod_A = Rod("A", WIDTH // 4)
        self.rod_B = Rod("B", WIDTH // 2)
        self.rod_C = Rod("C", (WIDTH * 3) // 4)

        for i in range(self.num_disks):
            width = BASE_WIDTH - (i * 20)
            color = DISK_COLORS[i]
            disk  = Disk(width, color)
            self.rod_A.push_disk(disk)

        self.moves = generate_hanoi_moves(self.num_disks)
        self.move_index = 0

        # Animation state
        self.animating = False
        self.anim_disk = None
        self.anim_phase = "lift"
        self.target_x = 0
        self.target_y = 0
        self.speed = 4

    def get_rod(self, name):
        if name == "A":
            return self.rod_A
        elif name == "B":
            return self.rod_B
        return self.rod_C

    def start_animation(self):
        # Start next move animation if there are moves left
        if self.move_index >= len(self.moves):
            return

        disk_num, from_rod, to_rod = self.moves[self.move_index]

        source = self.get_rod(from_rod)
        target = self.get_rod(to_rod)

        # Take top disk from source rod
        self.anim_disk = source.pop_disk()
        if self.anim_disk is None:
            return

        # Begin lift phase
        self.anim_phase = "lift"
        self.animating = True

        # Compute target x/y for final position
        self.target_x = target.x_pos - self.anim_disk.width // 2
        self.target_y = (150 + 350) - (len(target.disks) + 1) * DISK_HEIGHT

    def update_animation(self):
        # Do nothing if not animating
        if not self.animating or self.anim_disk is None:
            return

        # Lift phase: move disk up
        if self.anim_phase == "lift":
            self.anim_disk.y -= self.speed
            if self.anim_disk.y <= 100:
                self.anim_phase = "slide"

        # Slide phase: move disk horizontally toward target_x
        elif self.anim_phase == "slide":
            # Use tolerance so we don't get stuck never exactly equal
            if abs(self.anim_disk.x - self.target_x) > self.speed:
                if self.anim_disk.x < self.target_x:
                    self.anim_disk.x += self.speed
                else:
                    self.anim_disk.x -= self.speed
            else:
                # Snap to target_x and go to drop phase
                self.anim_disk.x = self.target_x
                self.anim_phase = "drop"

        # Drop phase: move disk down to target_y
        elif self.anim_phase == "drop":
            if self.anim_disk.y < self.target_y:
                self.anim_disk.y += self.speed
            else:
                # Finish move: place disk on target rod
                target = self.get_rod(self.moves[self.move_index][2])
                target.push_disk(self.anim_disk)

                # Reset animation state
                self.animating = False
                self.anim_disk = None
                self.move_index += 1

    def draw(self, surface):
        # Draw rods
        self.rod_A.draw(surface)
        self.rod_B.draw(surface)
        self.rod_C.draw(surface)

        # Draw disks on rods
        for rod in (self.rod_A, self.rod_B, self.rod_C):
            for disk in rod.disks:
                disk.draw(surface)

        # Draw animated disk if present
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

        # Buttons for control and speed
        self.buttons = [
            Button(50, 20, 120, 40, "Start"),
            Button(180, 20, 120, 40, "Pause"),
            Button(310, 20, 120, 40, "Resume"),
            Button(440, 20, 120, 40, "Slow"),
            Button(570, 20, 120, 40, "Medium"),
            Button(700, 20, 120, 40, "Fast" )
        ]

        # State: IDLE, RUNNING, PAUSED
        self.state = "IDLE"

    def draw(self):
        # Clear screen
        screen.fill(BG_COLOR)

        # Draw buttons
        for btn in self.buttons:
            btn.draw(screen)

        # Draw game (rods + disks + anim_disk)
        self.game.draw(screen)

        # Flip display
        pygame.display.flip()

    def handle_button_click(self, text):
        # Start auto animation
        if text == "Start":
            self.state = "RUNNING"

        # Pause animation
        elif text == "Pause":
            self.state = "PAUSED"

        # Resume animation
        elif text == "Resume":
            self.state = "RUNNING"

        # Speed controls
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

            # Auto animation: only when RUNNING
            if self.state == "RUNNING":
                if not self.game.animating:
                    self.game.start_animation()
                self.game.update_animation()

            # Draw everything
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    app = App()
    app.run()


