### Author: Andrei Sidorenko - 5750779
### Reviewer: Nael Karimou - 5734316

import math
import os
import pygame
from settings import *

class Furniture:
    '''a piece of furniture in the room that is not interactable, but still needs to be drawn with depth sorting.
    '''
    def __init__(self,room_name: str, name: str, obj_data: dict) -> None:
        self.name = name
        self.room_name = room_name
        
        # load the sprite
        path = os.path.join('assets',room_name, obj_data['path'])
        self.sprite = pygame.image.load(path).convert_alpha()

        # scale the sprite based on the scale factor in the data
        scaled_width = int(self.sprite.get_width() * obj_data['scale'])
        scaled_height = int(self.sprite.get_height() * obj_data['scale'])
        self.sprite = pygame.transform.scale(self.sprite,(scaled_width, scaled_height))

        # get the rectangle for the sprite, positioned at the x and y in the data
        self.rect = self.sprite.get_rect(topleft=(obj_data['position'][0] * SCREEN_WIDTH,
                                                  obj_data['position'][1] * SCREEN_HEIGHT))
        
        # define if object needs collision or not 
        self.collision = obj_data['collision']

        # load collision detection rectangle if needed
        if self.collision:  
            collision_rect_width = scaled_width
            collision_rect_height = self.sprite.get_height() // 10 # about 10% of object height

            collision_rect_pos = (
                obj_data['position'][0] * SCREEN_WIDTH,
                obj_data['position'][1] * SCREEN_HEIGHT +  (scaled_height - collision_rect_height)
            )
            self._collision_rect = pygame.Rect(collision_rect_pos, 
                                              (collision_rect_width, collision_rect_height)
            )

    def draw(self, surface: pygame.Surface) -> None:
        '''draw the furniture onto the given surface at the position of its rectangle'''
        surface.blit(self.sprite, self.rect)

    @property
    def collision_rect(self):
        '''
        Return the collision rectangle of the object
        '''
        return self._collision_rect
    
        
    def __repr__(self) -> str:
        return f"Furniture(name={self.name}, room={self.room_name})"

class InteractableObject(Furniture):
    '''
    An object the player can interact with by pressing E when nearby.
    inherits from Furniture because it also needs a sprite and rectangle for drawing and collision.
    Note that not all interactable objects need collision. Ex: cas file which seats on a desk.
    '''
    def __init__(self, room_name: str, name: str, obj_data: dict) -> None:
        super().__init__(room_name, name, obj_data)
        self._font = pygame.font.SysFont('Arial', 20)

    def draw(self, surface: pygame.Surface, player_center: tuple[int, int]) -> None:
        '''draw the object onto the given surface. also draws the [E] prompt if the player is near.'''
        surface.blit(self.sprite, self.rect)
        if self.is_player_near(player_center):
            self._draw_prompt(surface)

    def is_player_near(self, player_center: tuple[int, int]) -> bool:
        '''
        Check if the player is within the interaction radius of the object.
        Uses the center of the player's rectangle and the center of the object's rectangle to calculate distance.
        '''
        ox = self.rect.centerx
        oy = self.rect.centery
        px = player_center[0]
        py = player_center[1]
        dx = ox - px
        dy = oy - py
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance <= INTERACTION_RADIUS
    
    def _draw_prompt(self, surface):
        '''show [E] + name above the object'''
        text = "[E] " + self.name
        label = self._font.render(text, True, COLOUR_TEXT)
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

    def __repr__(self) -> str:
        return f"InteractableObject(name={self.name}, room={self.room_name})"
    

    
class Evidence(InteractableObject):
    '''
     A piece of evidence that the player can collect and view in the evidence bag. I
    Inherits from InteractableObject because it is something the player can interact with.
    '''
    def __init__(self, room_name: str, name: str, obj_data: dict) -> None:
        super().__init__(room_name, name, obj_data)
        self.collected = False
        self.visible = True 

    def draw(self, surface: pygame.Surface, player_center: tuple[int, int]) -> None:
        '''draw the evidence onto the given surface. also draws the [E] prompt if the player is near and has not collected it yet.'''
        if self.visible and not self.collected:
            super().draw(surface, player_center)
