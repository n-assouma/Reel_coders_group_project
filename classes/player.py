# Author: Andrei Sidorenko - 5750779
# Reviewer: Nael Karimou - 5734316

import os
import pygame
from settings import *


class Player:
    '''the player character that the user controls. Can move around with WASD.
    '''
    def __init__(self, player_data: dict) -> None:
        self._pos_x = player_data['position'][0] * SCREEN_WIDTH
        self._pos_y = player_data['position'][1] * SCREEN_HEIGHT
        self._speed = PLAYER_SPEED

        # load all the sprites for the player. We will switch between them to create a walking animation.
        
        front1_path = os.path.join('assets','sprites/detective_rowe', "front1.png")
        self.front1_sprite = pygame.image.load(front1_path).convert_alpha()
        PLAYER_WIDTH = self.front1_sprite.get_width() * player_data['scale'] 
        PLAYER_HEIGHT = self.front1_sprite.get_height() * player_data['scale']
        self.front1_sprite = pygame.transform.scale(self.front1_sprite, (PLAYER_WIDTH , PLAYER_HEIGHT)) 
        
        ###Amir H Javadi B - 5717292

        ###TODO: adjusting the scales

        front2_path = os.path.join('assets','sprites/detective_rowe', "front2.png")
        self.front2_sprite = pygame.image.load(front2_path).convert_alpha()
        self.front2_sprite = pygame.transform.scale(self.front2_sprite, (PLAYER_WIDTH  , PLAYER_HEIGHT))

        front3_path = os.path.join('assets','sprites/detective_rowe', "front3.png")
        self.front3_sprite = pygame.image.load(front3_path).convert_alpha()
        self.front3_sprite = pygame.transform.scale(self.front3_sprite, (PLAYER_WIDTH  , PLAYER_HEIGHT))

        back1_path = os.path.join('assets','sprites/detective_rowe', "back1.png")
        self.back1_sprite = pygame.image.load(back1_path).convert_alpha()
        self.back1_sprite = pygame.transform.scale(self.back1_sprite, (PLAYER_WIDTH   , PLAYER_HEIGHT)) 

        back2_path = os.path.join('assets','sprites/detective_rowe', "back2.png")
        self.back2_sprite = pygame.image.load(back2_path).convert_alpha()
        self.back2_sprite = pygame.transform.scale(self.back2_sprite, (PLAYER_WIDTH , PLAYER_HEIGHT +5))

        back3_path = os.path.join('assets','sprites/detective_rowe', "back3.png")
        self.back3_sprite = pygame.image.load(back3_path).convert_alpha()
        self.back3_sprite = pygame.transform.scale(self.back3_sprite, (PLAYER_WIDTH , PLAYER_HEIGHT + 5))

        left1_path = os.path.join('assets','sprites/detective_rowe', "left1.png")
        self.left1_sprite = pygame.image.load(left1_path).convert_alpha()
        self.left1_sprite = pygame.transform.scale(self.left1_sprite, (PLAYER_WIDTH   , PLAYER_HEIGHT)) 

        left2_path = os.path.join('assets','sprites/detective_rowe', "left2.png")
        self.left2_sprite = pygame.image.load(left2_path).convert_alpha()
        self.left2_sprite = pygame.transform.scale(self.left2_sprite, (PLAYER_WIDTH , PLAYER_HEIGHT))

        left3_path = os.path.join('assets','sprites/detective_rowe', "left3.png")
        self.left3_sprite = pygame.image.load(left3_path).convert_alpha()
        self.left3_sprite = pygame.transform.scale(self.left3_sprite, (PLAYER_WIDTH , PLAYER_HEIGHT))

        left4_path = os.path.join('assets','sprites/detective_rowe', "left4.png")
        self.left4_sprite = pygame.image.load(left4_path).convert_alpha()
        self.left4_sprite = pygame.transform.scale(self.left4_sprite, (PLAYER_WIDTH , PLAYER_HEIGHT))

        self.right1_sprite = pygame.transform.flip(self.left1_sprite, True, False)
        self.right2_sprite = pygame.transform.flip(self.left2_sprite, True, False)
        self.right3_sprite = pygame.transform.flip(self.left3_sprite, True, False)
        self.right4_sprite = pygame.transform.flip(self.left4_sprite, True, False)

        # loading the walking sound effect
        pygame.mixer.init()
        self.walk_sound = pygame.mixer.Sound(os.path.join("assets", "sprites", "detective_rowe", "walking_sound.mp3"))
        self.walk_sound.set_volume(0.1)
        self.is_walking = False

        ###Amir H Javadi B - 5717292

        # get the position rectangle for the sprite 
        self.rect = self.front1_sprite.get_rect(topleft=(self._pos_x, self._pos_y))
        
        # get collision rectangle for player
        collision_rect_width = PLAYER_WIDTH
        collision_rect_height = PLAYER_HEIGHT // 10 # about 10% of player height
        collision_rect_pos = (
            self._pos_x,
            self._pos_y + (PLAYER_HEIGHT - collision_rect_height)
        )
        self.collision_rect = pygame.Rect(collision_rect_pos,
                                        (collision_rect_width, collision_rect_height))
        
        # get next collision box for player next position computation
        self._next_pos_x = self.collision_rect.topleft[0]
        self._next_pos_y = self.collision_rect.topleft[1]
        

        self.x_direction = 0
        self.y_direction = 0
        self.animation_counter = 0
        self.last_movement = "u"

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

        ### Amir H Javadi B - 5717292

        #playing the walking sound effect if the player is moving, and stopping it if the player is not moving.
        if dx != 0 or dy != 0:
            if not self.is_walking:
                self.walk_sound.play(-1)  # -1 means loop
                self.is_walking = True
        else:
            self.walk_sound.stop()
            self.is_walking = False
        
        ### Amir H Javadi B - 5717292

        # define next position fror collision rectangle
        self._next_pos_x += dx
        self._next_pos_y += dy
        
        # define next position rectangle
        next_pos_rect = pygame.Rect(self._next_pos_x,
                                    self._next_pos_y,
                                    self.collision_rect.width,
                                    self.collision_rect.height)
        
        # check for collision
        collided = next_pos_rect.collidelist(collision_obj_lst) # return -1 if no collision

        # update position and rectangle
        if collided == -1: # if there was no collision
            #update player position
            self._pos_x += dx
            self._pos_y += dy
            self.rect.topleft = (self._pos_x,
                                 self._pos_y)
            
            #update collision rectangle position
            self.collision_rect = next_pos_rect
        
        else:
            # if there is a collision, reset next coordonate
            self._next_pos_x -= dx
            self._next_pos_y -= dy
        
        self.y_direction = dy
        self.x_direction = dx
        
    def draw(self, surface: pygame.Surface) -> None:
        '''draw the player onto the given surface. and showing the walking animation.'''

        ###Amir H Javadi B - 5717292

        if self.y_direction > 0:
            self.last_movement = "d"
            self.animation_counter += 1
            if self.animation_counter < 10: # change sprite every 10 frames
                frame = self.front2_sprite
            elif self.animation_counter < 20:
                frame = self.front3_sprite
            else:
                frame = self.front2_sprite
                self.animation_counter = 0
        
        elif self.y_direction < 0:
            self.last_movement = "u"
            self.animation_counter += 1
            if self.animation_counter < 10: # change sprite every 10 frames
                 frame = self.back2_sprite
            elif self.animation_counter < 20:
                frame = self.back3_sprite
            else:
                frame = self.back2_sprite
                self.animation_counter = 0
        
        elif self.x_direction > 0:
            self.last_movement = "r"
            self.animation_counter += 1
            if self.animation_counter < 5: # change sprite every 5 frames
                 frame = self.right1_sprite
            elif self.animation_counter < 10:
                frame = self.right2_sprite
            elif self.animation_counter < 15:
                frame = self.right3_sprite
            elif self.animation_counter < 20:
                frame = self.right4_sprite
            else:
                frame = self.right1_sprite
                self.animation_counter = 0
        elif self.x_direction < 0:
            self.last_movement = "l"
            self.animation_counter += 1
            if self.animation_counter < 5: # change sprite every 5 frames
                 frame = self.left1_sprite
            elif self.animation_counter < 10:
                frame = self.left2_sprite
            elif self.animation_counter < 15:
                frame = self.left3_sprite
            elif self.animation_counter < 20:
                frame = self.left4_sprite
            else:
                frame = self.left1_sprite
                self.animation_counter = 0
        else:        
            if self.last_movement == "u":
                frame = self.back1_sprite
            else: 
                frame = self.front1_sprite 

        rect = frame.get_rect(center=self.rect.center)
        surface.blit(frame, rect)
        ### Amir H Javadi B - 5717292

    def get_center(self) -> tuple[int, int]:
        '''get the center point of the player's rectangle. used for calculating distance to interactable objects.'''
        return self.rect.center

    def __repr__(self) -> str:
        return f"Player(pos=({self._pos_x}, {self._pos_y}))"
