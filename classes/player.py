
# player class
# humanoid body drawn with AI help
# 5750779

import pygame
from settings import *


class Player:
    # the player you can move with WASD

    def __init__(self, start_x, start_y):
        # starting rectangle
        self.rect = pygame.Rect(start_x, start_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.speed = PLAYER_SPEED
        # print("player created at", start_x, start_y)

    def handle_movement(self, keys, walls):
        # figure out how much to move
        dx = 0
        dy = 0

        # left
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
        # right
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
        # up
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
        # down
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed

        # move x first then check for walls
        self.rect.x = self.rect.x + dx
        for w in walls:
            if self.rect.colliderect(w):
                if dx > 0:
                    # moving right, push back to the left side of the wall
                    self.rect.right = w.left
                if dx < 0:
                    # moving left, push back to the right side of the wall
                    self.rect.left = w.right

        # move y after then check for walls
        self.rect.y = self.rect.y + dy
        for w in walls:
            if self.rect.colliderect(w):
                if dy > 0:
                    self.rect.bottom = w.top
                if dy < 0:
                    self.rect.top = w.bottom

    def draw(self, surface):
        # draw humanoid player (AI)

        # little oval shadow on the ground
        shadow_y = self.rect.bottom - 3
        shadow_rect = pygame.Rect(self.rect.centerx - 12, shadow_y, 24, 6)
        pygame.draw.ellipse(surface, (0, 0, 0, 80), shadow_rect)

        # coat (body) — about 60% of the player height
        body_height = int(PLAYER_HEIGHT * 0.6)
        body_x = self.rect.x
        body_y = self.rect.bottom - body_height
        body_rect = pygame.Rect(body_x, body_y, PLAYER_WIDTH, body_height)
        pygame.draw.rect(surface, COLOUR_PLAYER_BODY, body_rect)

        # dark line down the middle (buttons)
        line_x = body_rect.centerx
        pygame.draw.line(
            surface, COLOUR_PLAYER_DARK,
            (line_x, body_rect.top),
            (line_x, body_rect.bottom),
            1,
        )

        # dark strip at the bottom of the coat
        bottom_strip = pygame.Rect(body_rect.x, body_rect.bottom - 3, PLAYER_WIDTH, 3)
        pygame.draw.rect(surface, COLOUR_PLAYER_DARK, bottom_strip)

        # head (circle on top)
        head_r = 9
        head_x = self.rect.centerx
        head_y = self.rect.top + head_r + 2
        pygame.draw.circle(surface, COLOUR_PLAYER_HEAD, (head_x, head_y), head_r)

        # hair (dark ellipse on the top half of the head)
        hair_rect = pygame.Rect(
            head_x - head_r, head_y - head_r,
            head_r * 2, head_r + 2,
        )
        pygame.draw.ellipse(surface, COLOUR_PLAYER_HAIR, hair_rect)

    def get_center(self):
        # give back the middle point
        return self.rect.center
