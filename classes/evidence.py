### Author: Nael Karimou 5734316
### Co-author(s): ...

import pygame

from .interactable_object import InteractableObject


class Evidence(InteractableObject):
    '''
    A piece of evidence that the player can collect and view in the evidence bag.
    It inherits from InteractableObject.

    Methods:
        Evidence.draw(): draw evidence object and examination '[E] ...' prompt on a surface

        Inherit methods from Interactable object

    Attribute:
        Evidence.collected (bool): is true if evidence is collected by player, false otherwise

        Evidence.visible (bool): is evidence should be drawn to screen, false otherwise
    
        Inherit attribute from InteractableObject

    '''
    def __init__(self, room_name: str, name: str, obj_data: dict) -> None:
        super().__init__(room_name, name, obj_data)
        self.collected = False
        self.visible = True 

    def draw(self, surface: pygame.Surface, player_center: tuple[int, int]) -> None:
        '''draw the evidence onto the given surface. also draws the [E] prompt if the player is near and has not collected it yet.'''
        if self.visible and not self.collected:
            super().draw(surface, player_center)
