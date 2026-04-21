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

        # get the position rectangle for the sprite 
        self.rect = self.sprite.get_rect(topleft=(self._pos_x * SCREEN_WIDTH,
                                                  self._pos_y * SCREEN_HEIGHT))
        
        # get collision rectangle for player
        collision_rect_width = PLAYER_WIDTH
        collision_rect_height = PLAYER_HEIGHT // 10 # about 10% of player height

        collision_rect_pos = (
            self._pos_x * SCREEN_WIDTH,
            self._pos_y * SCREEN_HEIGHT + (PLAYER_HEIGHT - collision_rect_height)
        )

        self.collision_rect = pygame.Rect(collision_rect_pos,
                                        (collision_rect_width, collision_rect_height))
        

    def handle_movement(self, pressed_keys: list, collision_obj_lst: list) -> None: 
        '''handle player movement based on user input and detect collision.
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

        # define next position
        next_pos_x = self.collision_rect.topleft[0] + dx,
        next_pos_y = self.collision_rect.topleft[1] + dy
        
        # define next position rectangle
        next_pos_rect = pygame.Rect(next_pos_x,
                                    next_pos_y,
                                    self.collision_rect.width,
                                    self.collision_rect.height)
        
        # check for collision
        collided = next_pos_rect.collidelist(collision_obj_lst) # return -1 if no collision

        # update position and rectangle
        if collided == -1: # if there was no collision
            self._pos_x = next_pos_x
            self._pos_y = next_pos_y
            self.rect.topleft = (self._pos_x, self._pos_y)


    def draw(self, surface: pygame.Surface) -> None:
        '''draw the player onto the given surface.'''
        surface.blit(self.sprite, self.rect.topleft)

    def get_center(self) -> tuple[int, int]:
        '''get the center point of the player's rectangle. used for calculating distance to interactable objects.'''
        return self.rect.center

    def __repr__(self) -> str:
        return f"Player(pos=({self._pos_x}, {self._pos_y}))"
