
# hud class (bottom panel with chief hint, notepad, and evidence)
# 5750779

from .interactable_object import InteractableObject
import pygame
from .evidence_bag import EvidenceBag
from .chief_of_police_hint import ChiefOfPoliceHint
from settings import *


class HUD:
    # the bottom strip with 3 panels

    def __init__(self, evidence_bag: EvidenceBag, chief_hint: ChiefOfPoliceHint, map: InteractableObject) -> None:
        # fonts (these look better than the default)
        # used by the evidence panel below
        self.font_title = pygame.font.SysFont("Segoe UI,Arial", 15, bold=True)
        self.font_body = pygame.font.SysFont("Segoe UI,Arial", 14)
        self.font_small = pygame.font.SysFont("Segoe UI,Arial", 12)
        self.evidence_bag = evidence_bag
        
        # set chief of police
        self.chief_hint = chief_hint
        
        #set map 
        self.map = map
        self.map_rect = pygame.Rect(0, 0, 80, 50)

    def set_hint(self, text):
        # forward the hint text to the chief panel
        self.chief_hint.set_hint(text)

    def draw(self, surface, active_evidence=None):
        # draw the hud background + 3 panels

        # big background box for the whole hud
        pygame.draw.rect(surface, COLOUR_HUD_BG, (0, MAIN_SCREEN_HEIGHT, SCREEN_WIDTH, HUD_HEIGHT))
        # thin line between the game and the hud
        pygame.draw.line(surface, COLOUR_HUD_BORDER, (0, MAIN_SCREEN_HEIGHT), (SCREEN_WIDTH, MAIN_SCREEN_HEIGHT), 2)

        # figure out the size of each of the 3 panels
        pad = 12
        width = (SCREEN_WIDTH - pad * 3)
        panel1_w = width * 6 // 10
        panel2_w = width * 4 // 10
        panel_y = MAIN_SCREEN_HEIGHT + pad
        panel_h = HUD_HEIGHT - pad * 2

        # panel 1: chief of police - drawn by the ChiefOfPoliceHint class
        panel1_x = pad
        self.chief_hint.draw(surface, panel1_x, panel_y, panel1_w, panel_h)

### Amir H Javadi B 5717292 - start

        # panel 2: evidence bag
        items_number = len(self.evidence_bag)
        panel2_x = panel1_x + panel1_w + pad
        self.draw_panel(surface, panel2_x, panel_y, panel2_w, panel_h,
                        f"EVIDENCE BAG  ({items_number} / {self.evidence_bag.MAX_SIZE})",
                        COLOUR_TEXT_EVIDENCE,
                        "" if items_number > 0 else "No evidence collected yet.",
                        COLOUR_TEXT_DIM)

        # Starting position for the first evidence item icon in the grid
        img_x = panel2_x + pad + 80
        img_y = panel_y + 42

        # Draw the trash can icon and update its rect for click detection
        trash_pos = (panel2_x - 3*pad, panel_y + panel_h - 120)
        surface.blit(self.evidence_bag.trash_can_image, trash_pos)
        self.evidence_bag.trash_can_rect.topleft = trash_pos

        # Draw the map icon and update its rect for click detection
        map_pos = (panel2_x + pad - 120, panel_y + panel_h - 130)
        map_scaled = pygame.transform.scale(self.map.sprite, (80, 50))
        surface.blit(map_scaled, map_pos)
        self.map_rect = pygame.Rect(map_pos[0], map_pos[1], 80, 50)

        if self.evidence_bag.is_open:
            # Show full or empty bag icon depending on whether items exist
            bag_pos = (panel2_x + panel2_w - 150, panel_y + panel_h - 145)
            if len(self.evidence_bag.items):
                surface.blit(self.evidence_bag.full_opened_bag_image, bag_pos)
            else:
                surface.blit(self.evidence_bag.empty_opened_bag_image, bag_pos)

            for num, evidence in enumerate(self.evidence_bag.items):
                scaled = pygame.transform.scale(evidence.sprite, (50, 50))
                if num == active_evidence:
                    # Dragged item stays at its current rect position
                    surface.blit(scaled, evidence.rect.topleft)
                else:
                    surface.blit(scaled, (img_x, img_y))
                    # Update rect so click detection stays in sync with drawn position
                    evidence.rect = pygame.Rect(img_x, img_y, 50, 50)

                # After 3 items, wrap to a second row
                if num == 2:
                    img_x = panel2_x + pad + 40
                    img_y = panel_y + 100

                # Advance to the next item slot horizontally
                img_x += 80
        else:
            # Bag is closed — show the closed bag icon
            bag_pos = (panel2_x + panel2_w - 150, panel_y + panel_h - 145)
            surface.blit(self.evidence_bag.closed_bag_image, bag_pos)

        # Always update the bag rect so clicking it works regardless of open state
        self.evidence_bag.rect.topleft = (
            panel2_x + panel2_w - 150, panel_y + panel_h - 145
        )

### Amir H Javadi B 5717292 - end

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
