
# objects the player can press E on
# 5750779

import math
import pygame
from settings import *


class InteractableObject:
    # an object in the room (paper, lamp, door, etc.)
    # the "kind" tells draw() which style to draw

    def __init__(self, x, y, width, height, name, clue_id=None, kind="generic"):
        # save position, size and info
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.clue_id = clue_id
        self.kind = kind

    def is_player_near(self, player_center):
        # true if the player is within the interact radius
        # using pythagoras to get the distance
        ox = self.rect.centerx
        oy = self.rect.centery
        px = player_center[0]
        py = player_center[1]
        dx = ox - px
        dy = oy - py
        distance = math.sqrt(dx * dx + dy * dy)
        return distance <= INTERACTION_RADIUS

    def draw(self, surface, is_near, font):
        # pick a style based on the kind
        if self.kind == "door":
            self.draw_door(surface, is_near)
        elif self.kind == "paper":
            self.draw_paper(surface, is_near)
        elif self.kind == "lamp":
            self.draw_lamp(surface, is_near)
        elif self.kind == "board":
            self.draw_board(surface, is_near)
        elif self.kind == "computer":
            self.draw_computer(surface, is_near)
        else:
            self.draw_generic(surface, is_near)

        # when the player is close, show [E] name above it
        if is_near:
            self.draw_prompt(surface, font)

    def draw_generic(self, surface, is_near):
        # just a yellow rectangle
        if is_near:
            colour = COLOUR_HIGHLIGHT
        else:
            colour = COLOUR_OBJECT
        pygame.draw.rect(surface, colour, self.rect, border_radius=3)
        pygame.draw.rect(surface, COLOUR_OBJECT_DARK, self.rect, 2, border_radius=3)

    def draw_paper(self, surface, is_near):
        # white paper (AI)
        if is_near:
            colour = (255, 250, 210)
        else:
            colour = (250, 240, 215)
        pygame.draw.rect(surface, colour, self.rect, border_radius=1)
        pygame.draw.rect(surface, (180, 160, 120), self.rect, 1)
        # fold line in the middle
        pygame.draw.line(
            surface, (200, 180, 140),
            (self.rect.x + 4, self.rect.centery),
            (self.rect.right - 4, self.rect.centery),
            1,
        )

    def draw_lamp(self, surface, is_near):
        # desk lamp (AI)
        # small base
        base_rect = pygame.Rect(self.rect.centerx - 4, self.rect.bottom - 6, 8, 6)
        pygame.draw.rect(surface, (60, 40, 30), base_rect)

        # lamp shade
        if is_near:
            shade_colour = COLOUR_HIGHLIGHT
        else:
            shade_colour = COLOUR_OBJECT
        shade_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height - 8)
        pygame.draw.ellipse(surface, shade_colour, shade_rect)
        pygame.draw.ellipse(surface, COLOUR_OBJECT_DARK, shade_rect, 2)

        # glow when the player is near
        if is_near:
            glow = pygame.Rect(self.rect.centerx - 20, self.rect.centery - 14, 40, 28)
            pygame.draw.ellipse(surface, (255, 220, 120, 40), glow, 1)

    def draw_door(self, surface, is_near):
        # door (AI)
        if is_near:
            colour = (180, 120, 70)
        else:
            colour = COLOUR_DOOR
        pygame.draw.rect(surface, colour, self.rect, border_radius=2)
        pygame.draw.rect(surface, COLOUR_DOOR_DARK, self.rect, 2, border_radius=2)

        # two panels on the door
        panel_pad = 4
        panel_w = self.rect.width - panel_pad * 2
        panel_h = (self.rect.height - panel_pad * 3) // 2
        i = 0
        while i < 2:
            px = self.rect.x + panel_pad
            py = self.rect.y + panel_pad + i * (panel_h + panel_pad)
            panel_rect = pygame.Rect(px, py, panel_w, panel_h)
            pygame.draw.rect(surface, COLOUR_DOOR_DARK, panel_rect, 1)
            i = i + 1

        # knob
        pygame.draw.circle(surface, (220, 180, 80), (self.rect.right - 6, self.rect.centery), 2)

    def draw_board(self, surface, is_near):
        # suspects board with 3 little cards (AI)
        if is_near:
            colour = (140, 95, 55)
        else:
            colour = (110, 75, 45)
        pygame.draw.rect(surface, colour, self.rect, border_radius=2)
        pygame.draw.rect(surface, (60, 40, 20), self.rect, 2, border_radius=2)

        # 3 cards pinned to the board
        card_w = 18
        card_h = 24
        gap = (self.rect.width - card_w * 3) // 4
        i = 0
        while i < 3:
            cx = self.rect.x + gap + i * (card_w + gap)
            cy = self.rect.y + 6
            pygame.draw.rect(surface, (240, 230, 210), (cx, cy, card_w, card_h))
            pygame.draw.rect(surface, (160, 140, 110), (cx, cy, card_w, card_h), 1)
            i = i + 1

    def draw_computer(self, surface, is_near):
        # computer (AI)
        pygame.draw.rect(surface, (50, 50, 60), self.rect, border_radius=2)
        pygame.draw.rect(surface, (25, 25, 30), self.rect, 2, border_radius=2)
        # screen area (smaller than the case)
        screen_rect = self.rect.inflate(-6, -6)
        # screen lights up when the player is near
        if is_near:
            screen_colour = (80, 200, 140)
        else:
            screen_colour = (40, 100, 70)
        pygame.draw.rect(surface, screen_colour, screen_rect)

    def draw_prompt(self, surface, font):
        # show [E] + name above the object
        text = "[E] " + self.name
        label = font.render(text, True, COLOUR_TEXT)
        pad = 6
        bg_rect = label.get_rect()
        bg_rect.centerx = self.rect.centerx
        bg_rect.bottom = self.rect.top - 8
        bg_rect.inflate_ip(pad * 2, pad)
        # dark rounded box behind the text
        pygame.draw.rect(surface, (20, 18, 24), bg_rect, border_radius=4)
        pygame.draw.rect(surface, COLOUR_HIGHLIGHT, bg_rect, 1, border_radius=4)
        # center the text inside the box
        label_rect = label.get_rect(center=bg_rect.center)
        surface.blit(label, label_rect)
