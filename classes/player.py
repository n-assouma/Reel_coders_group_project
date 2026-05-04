# Author: Andrei Sidorenko - 5750779
# Reviewer: Nael Karimou - 5734316

import os
import pygame
from settings import *


class Player:
    '''the player character that the user controls. Can move around with WASD.
    '''
    def __init__(self, player_data: dict, walkable_area_info: dict) -> None:
        self._pos_x = player_data['position'][0] * SCREEN_WIDTH
        self._pos_y = player_data['position'][1] * SCREEN_HEIGHT
        self._speed = PLAYER_SPEED

        # load the sprite
        path = os.path.join('assets','sprites', 'detective_rowe', player_data['sprite'])
        self.sprite = pygame.image.load(path).convert_alpha()
        PLAYER_WIDTH = self.sprite.get_width() * player_data['scale']
        PLAYER_HEIGHT = self.sprite.get_height() * player_data['scale']
        self.sprite = pygame.transform.scale(self.sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))

        # get the position rectangle for the sprite 
        self.rect = self.sprite.get_rect(topleft=(self._pos_x, self._pos_y))

        # load background walkable area rectangle
        self.walkable_area_rect = pygame.Rect(walkable_area_info['top_left'][0] * SCREEN_WIDTH,
                                             walkable_area_info['top_left'][1] * SCREEN_HEIGHT,
                                             walkable_area_info['width'] * SCREEN_WIDTH,
                                             walkable_area_info['height'] * SCREEN_HEIGHT)
        
        # get collision rectangle for player
        collision_rect_width = PLAYER_WIDTH
        collision_rect_height = PLAYER_HEIGHT // 10 # about 10% of player height
        collision_rect_pos = (
            self._pos_x,
            self._pos_y + (PLAYER_HEIGHT - collision_rect_height)
        )
        self.collision_rect = pygame.Rect(collision_rect_pos,
                                        (collision_rect_width, collision_rect_height))
        
        # define next collision coordonate for player next position computation
        self._next_pos_x = self.collision_rect.topleft[0]
        self._next_pos_y = self.collision_rect.topleft[1]

        # define position for vertical sorting
        self.y_sort_pos = self.rect.bottomleft[1]
        

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

        # define next position fror collision rectangle
        self._next_pos_x += dx
        self._next_pos_y += dy
        
        # define next position rectangle
        next_collision_rect = pygame.Rect(self._next_pos_x,
                                    self._next_pos_y,
                                    self.collision_rect.width,
                                    self.collision_rect.height)
        
        # check if player is inside walkable area i.e not colliding with a wall
        not_collide_with_wall = self.walkable_area_rect.contains(next_collision_rect)
        
        # check for collision with furniture
        collide_with_objects = False if next_collision_rect.collidelist(collision_obj_lst) == -1 else True

        # update position and rectangle
        if not collide_with_objects and not_collide_with_wall: # if there was no collision
            #update player position
            self._pos_x += dx
            self._pos_y += dy
            self.rect.topleft = (self._pos_x,
                                 self._pos_y)
            # update player position for y sorting
            self.y_sort_pos = self.rect.bottomleft[1]
            
            #update collision rectangle position
            self.collision_rect = next_collision_rect
        
        else:
            # if there is a collision, reset next coordonate
            self._next_pos_x -= dx
            self._next_pos_y -= dy
        

    def draw(self, surface: pygame.Surface) -> None:
        '''draw the player onto the given surface.'''
        surface.blit(self.sprite, self.rect.topleft)

    def get_center(self) -> tuple[int, int]:
        '''get the center point of the player's rectangle. used for calculating distance to interactable objects.'''
        return self.rect.center

    def __repr__(self) -> str:
        return f"Player(pos=({self._pos_x}, {self._pos_y}))"
