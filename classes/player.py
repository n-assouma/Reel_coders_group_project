# Author: Andrei Sidorenko - 5750779
# Reviewer: Nael Karimou - 5734316

import os
import pygame
from settings import *


class Player:
    '''the player character that the user controls. Can move around with WASD.
    '''
    def __init__(self, player_data: dict) -> None:
        self._pos = self._pos_x, self._pos_y = player_data['position']
        self._speed = PLAYER_SPEED

        # load the sprite
        path = os.path.join('assets','sprites', 'detective_rowe', player_data['sprite'])
        self.sprite = pygame.image.load(path).convert_alpha()
        PLAYER_WIDTH = self.sprite.get_width() * player_data['scale']
        PLAYER_HEIGHT = self.sprite.get_height() * player_data['scale']
        self.sprite = pygame.transform.scale(self.sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))

        # get the rectangle for the sprite 
        self.rect = self.sprite.get_rect(topleft=(self._pos_x * SCREEN_WIDTH,
                                                  self._pos_y * SCREEN_HEIGHT))

    def handle_movement(self, pressed_keys: list) -> None: 
        '''handle player movement based on user input.
        TODO: Add collision detection
        TODO: make movement speed independent of FPS so that 
        it is consistent across different machines. maybe use delta time?
        '''
        dx = dy = 0
        if pressed_keys[pygame.K_w]:
            dy = -self._speed
        if pressed_keys[pygame.K_s]:
            dy = self._speed
        if pressed_keys[pygame.K_a]:
            dx = -self._speed
        if pressed_keys[pygame.K_d]:
            dx = self._speed

        # update position and rectangle
        self._pos_x += dx
        self._pos_y += dy
        self.rect.topleft = (self._pos_x * SCREEN_WIDTH, self._pos_y * SCREEN_HEIGHT)

    def draw(self, surface: pygame.Surface) -> None:
        '''draw the player onto the given surface.'''
        surface.blit(self.sprite, self.rect.topleft)

    def get_center(self) -> tuple[int, int]:
        '''get the center point of the player's rectangle. used for calculating distance to interactable objects.'''
        return self.rect.center

    def __repr__(self) -> str:
        return f"Player(pos=({self._pos_x}, {self._pos_y}))"
