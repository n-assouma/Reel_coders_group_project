### Author: Nael Karimou 5734316

import pygame

from .interactable_object import InteractableObject


class Evidence(InteractableObject):
    '''
    A piece of evidence that the player can collect and view in the evidence bag.
    It inherits from InteractableObject.
    '''
    def __init__(self, room_name: str, name: str, obj_data: dict) -> None:
        super().__init__(room_name, name, obj_data)
        self.collected = False
        self.visible = True 
        self.priority: int = obj_data['priority']

    def draw(self, surface: pygame.Surface, player_center: tuple[int, int]) -> None:
        '''draw the evidence onto the given surface. also draws the [E] prompt if the player is near and has not collected it yet.'''
        if self.visible and not self.collected:
            super().draw(surface, player_center)

class NPC(InteractableObject):
    '''
    A non-player character that the player can interact with by pressing E when nearby.
    The player can also drop evidence on him to get a reaction.
    inherits from InteractableObject because it also needs a sprite and rectangle for drawing and collision.
    '''
    def __init__(self, room_name: str, name: str, obj_data: dict) -> None:
        super().__init__(room_name, name, obj_data)

### Nael Karimou - 5734316