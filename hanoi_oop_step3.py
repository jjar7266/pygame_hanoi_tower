# OOP Step 3: Add Button class and UI controls.
# This step adds:
#  - Button class
#  - Start, Pause, Resume, Next, Back, Manual buttons
#  - Button drawing
#  - Button clicking
# No animation yet. BUttons only call game methods.

# Import modules
import pygame
import sys
from hanoi_logic import generate_hanoi_moves

# Initialize Pygame
pygame.init()

# Create the display window
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi - OOP Step 3")

# COLORS
BG_COLOR   = ("#1e1e1e")
ROD_COLOR  = ("#c8c8c8")
BTN_COLOR  = ("#3c3c3c")
BTN_HOVER  = ("#646464")
TEXT_COLOR = ("#e6e6e6")
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


    def get_rod(self, name):
        if name == "A":
            return self.rod_A
        elif name == "B":
            return self.rod_B
        return self.rod_C

    def do_next_move(self):
        if self.move_index >= len(self.moves):
            return

        disk_num, from_rod, to_rod = self.moves[self.move_index]

        source = self.get_rod(from_rod)
        target = self.get_rod(to_rod)

        disk = source.pop_disk()
        target.push_disk(disk)

        self.move_index += 1

    def do_back_move(self):
        if self.move_index <= 0:
            return

        self.move_index -= 1
        disk_num, from_rod, to_rod = self.moves[self.move_index]

        source = self.get_rod(to_rod)
        target = self.get_rod(from_rod)

        disk = source.pop_disk()
        target.push_disk(disk)

    def draw(self, surface):
        self.rod_A.draw(surface)
        self.rod_B.draw(surface)
        self.rod_C.draw(surface)

        for rod in (self.rod_A, self.rod_B, self.rod_C):
            for disk in rod.disks:
                disk.draw(surface)


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
            Button(50, 20, 120, 40, "Start"),
            Button(180, 20, 120, 40, "Pause"),
            Button(310, 20, 120, 40, "Resume"),
            Button(440, 20, 120, 40, "Next"),
            Button(570, 20, 120, 40, "Back"),
            Button(700, 20, 150, 40, "Manual Mode")
        ]

        # State: IDLE, AUTO, MANUAL, PAUSED
        self.state = "IDLE"

        # Slow AUTO mode using a timer (600ms)
        self.MOVE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE_EVENT, 600)

    def draw(self):
        screen.fill(BG_COLOR)

        for btn in self.buttons:
            btn.draw(screen)

        self.game.draw(screen)

        pygame.display.flip()

    def handle_button_click(self, text):
        if text == "Start":
            # Auto mode: keep stepping forward each frame
            self.state = "AUTO"

        elif text == "Pause":
            self.state = "PAUSED"

        elif text == "Resume":
            # Resume auto mode
            self.state = "AUTO"

        elif text == "Next":
            # Manual single forward step
            if self.state == "MANUAL":
                self.game.do_next_move()

        elif text == "Back":
            # Manual single backward step
            if self.state == "MANUAL":
                self.game.do_back_move()

        elif text == "Manual Mode":
            # Switch to manual mode (no auto stepping)
            self.state = "MANUAL"

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Timer-driven AUTO stepping
                if event.type == self.MOVE_EVENT:
                    if self.state == "AUTO":
                        self.game.do_next_move()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    for btn in self.buttons:
                        if btn.is_clicked(mx, my):
                            self.handle_button_click(btn.text)

            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    app = App()
    app.run()



