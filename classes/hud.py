
# hud class (bottom panel with chief hint, notepad, and evidence)
# 5750779

import pygame
from settings import *

# TODO: make the notepad actually work so the player can type in it


class HUD:
    # the bottom strip with 3 panels

    def __init__(self):
        # starting hint
        self.current_hint = "Walk around with WASD. Get close to objects and press E."
        # fonts (these look better than the default)
        self.font_title = pygame.font.SysFont("Segoe UI,Arial", 15, bold=True)
        self.font_body = pygame.font.SysFont("Segoe UI,Arial", 14)
        self.font_small = pygame.font.SysFont("Segoe UI,Arial", 12)

    def set_hint(self, text):
        # change the chief of police hint
        self.current_hint = text

    def draw(self, surface):
        # draw the hud background + 3 panels

        # big background box for the whole hud
        pygame.draw.rect(surface, COLOUR_HUD_BG, (0, MAIN_SCREEN_HEIGHT, SCREEN_WIDTH, HUD_HEIGHT))
        # thin line between the game and the hud
        pygame.draw.line(surface, COLOUR_HUD_BORDER, (0, MAIN_SCREEN_HEIGHT), (SCREEN_WIDTH, MAIN_SCREEN_HEIGHT), 2)

        # figure out the size of each of the 3 panels
        pad = 12
        panel_w = (SCREEN_WIDTH - pad * 4) // 3
        panel_y = MAIN_SCREEN_HEIGHT + pad
        panel_h = HUD_HEIGHT - pad * 2

        # panel 1: chief of police
        x1 = pad
        self.draw_panel(surface, x1, panel_y, panel_w, panel_h,
                        "CHIEF OF POLICE", COLOUR_TEXT_CHIEF,
                        self.current_hint, COLOUR_TEXT)

        # panel 2: notepad
        x2 = x1 + panel_w + pad
        self.draw_panel(surface, x2, panel_y, panel_w, panel_h,
                        "NOTEPAD", COLOUR_TEXT_NOTEPAD,
                        "Type your own notes here. (coming soon)", COLOUR_TEXT_DIM)

        # panel 3: evidence bag
        x3 = x2 + panel_w + pad
        self.draw_panel(surface, x3, panel_y, panel_w, panel_h,
                        "EVIDENCE BAG  (0 / 5)", COLOUR_TEXT_EVIDENCE,
                        "No evidence collected yet. (Amirhoseinj is building this)", COLOUR_TEXT_DIM)

    def draw_panel(self, surface, x, y, w, h, title, title_colour, body, body_colour):
        # draw one panel on the hud

        # background box
        panel_rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, COLOUR_HUD_PANEL, panel_rect, border_radius=6)
        pygame.draw.rect(surface, COLOUR_HUD_BORDER, panel_rect, 1, border_radius=6)

        # small accent bar next to the title
        accent_bar = pygame.Rect(x + 10, y + 10, 3, 16)
        pygame.draw.rect(surface, title_colour, accent_bar, border_radius=1)

        # title text
        title_surf = self.font_title.render(title, True, title_colour)
        surface.blit(title_surf, (x + 20, y + 9))

        # divider line under the title
        pygame.draw.line(surface, COLOUR_HUD_BORDER, (x + 10, y + 32), (x + w - 10, y + 32), 1)

        # body text — wrap it so it fits in the panel
        text_x = x + 12
        text_y = y + 42
        max_w = w - 24

        # split text into words and put them on lines
        words = body.split(" ")
        line = ""
        line_h = 19
        for word in words:
            test = (line + " " + word).strip()
            width, _ = self.font_body.size(test)
            if width <= max_w:
                line = test
            else:
                # this line is full, draw it and start a new one
                rendered = self.font_body.render(line, True, body_colour)
                surface.blit(rendered, (text_x, text_y))
                text_y = text_y + line_h
                line = word
        # draw the last line if theres anything left
        if line != "":
            rendered = self.font_body.render(line, True, body_colour)
            surface.blit(rendered, (text_x, text_y))
