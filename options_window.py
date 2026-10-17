# ------------------------------------------------------------
# options_window.py
# Step 8 - Tower of Hanoi
# Modal popup window drawn INSIDE the main window.
#
# This window:
#   • Pauses the main game
#   • Draws a dark overlay
#   • Draws a centered popup box
#   • Lets the user change:
#         - Mode (AUTO / MANUAL)
#         - Speed (Slow / Medium / Fast)
#         - Disk Count (3–6)
#   • Apply & Close returns settings to the main App
# ------------------------------------------------------------

# Import modules
import pygame

# Initialize Pygame
pygame.init()

# Simple button class for the popup
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()

        color = (180, 180, 180)
        if self.rect.collidepoint(mouse):
            color = (220, 220, 220)

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (40, 40, 40), self.rect, 3)

        font = pygame.font.SysFont(None, 28)
        txt = font.render(self.text, True, (0, 0, 0))
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 8))

    def is_clicked(self, mx, my):
        return self.rect.collidepoint(mx, my)


# optionsWindow: popup window
class OptionsWindow:
    """
    This class draws a modal popup INSIDE the main window.
    It does NOT create a second Pygame window.
    """

    def __init__(self, app):
        # reference to main App so we can modify settings
        self.app = app
        self.screen = app.screen

        # popup window size
        self.width  = 500
        self.height = 420

        # Center the popup
        self.popup_x = (self.app.WIDTH - self.width) // 2
        self.popup_y = (self.app.HEIGHT - self.height) // 2

        # temporary settings (not applied until "Apply & Close")
        self.temp_mode  = app.state
        self.temp_speed = app.game.speed
        self.temp_disks = app.game.num_disks

        # Build buttons
        self.buttons = []
        self.build_buttons()

        self.running = True

    def build_buttons(self):
        px = self.popup_x
        py = self.popup_y

        # Mode buttons
        self.buttons.append(Button(px + 50,  py + 60, 180, 40, "Mode: AUTO"))
        self.buttons.append(Button(px + 270, py + 60, 180, 40, "Mode: MANUAL"))

        # Speed buttons
        self.buttons.append(Button(px + 50,  py + 140, 180, 40, "Speed: Slow"))
        self.buttons.append(Button(px + 270, py + 140, 180, 40, "Speed: Medium"))
        self.buttons.append(Button(px + 50,  py + 200, 180, 40, "Speed: Fast"))

        # Disk buttons
        self.buttons.append(Button(px + 50,  py + 280, 100, 40, "Disks: 3"))
        self.buttons.append(Button(px + 160, py + 280, 100, 40, "Disks: 4"))
        self.buttons.append(Button(px + 270, py + 280, 100, 40, "Disks: 5"))
        self.buttons.append(Button(px + 380, py + 280, 100, 40, "Disks: 6"))

        # Apply & Close
        self.buttons.append(Button(px + 150, py + 340, 200, 50, "Apply & Close"))

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def draw(self):
        # Dark overlay
        overlay = pygame.Surface((self.app.WIDTH, self.app.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Popup box
        pygame.draw.rect(self.screen, (40, 40, 40),
                         (self.popup_x, self.popup_y, self.width, self.height))
        pygame.draw.rect(self.screen, (200, 200, 200),
                         (self.popup_x, self.popup_y, self.width, self.height), 3)

        # Title
        font = pygame.font.SysFont(None, 36)
        title = font.render("Options", True, (255, 255, 255))
        self.screen.blit(title, (self.popup_x + 180, self.popup_y + 15))

        # Draw all buttons
        for btn in self.buttons:
            btn.draw(self.screen)

    # ----------------------------------------------------------------
    # handle clicks inside popup
    # ----------------------------------------------------------------
    def handle_click(self, text):
        # Mode
        if text == "Mode: AUTO":
            self.temp_mode = "AUTO"

        elif text == "Mode: MANUAL":
            self.temp_mode = "MANUAL"

        # Speed
        elif text == "Speed: Slow":
            self.temp_speed = 2

        elif text == "Speed: Medium":
            self.temp_speed = 4

        elif text == "Speed: Fast":
            self.temp_speed = 8

        # Disk count
        elif text == "Disks: 3":
            self.temp_disks = 3
        elif text == "Disks: 4":
            self.temp_disks = 4
        elif text == "Disks: 5":
            self.temp_disks = 5
        elif text == "Disks: 6":
            self.temp_disks = 6

        # Apply & Close
        elif text == "Apply & Close":
            self.apply_changes()
            self.running = False

    def apply_changes(self):
        # Apply mode
        if self.app.state != self.temp_mode:
            self.app.state = self.temp_mode
            self.app.game.reset()

        # Apply speed
        self.app.game.speed = self.temp_speed

        # Apply disk count (rebuild game)
        if self.temp_disks != self.app.game.num_disks:
            self.app.game = self.app.game.__class__(self.temp_disks)

    # -----------------------------------------------------------------
    # run popup loop
    # -----------------------------------------------------------------
    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.app.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        if btn.is_clicked(mx, my):
                            self.handle_click(btn.text)

            # Draw popup
            self.draw()

            pygame.display.flip()
            clock.tick(60)
