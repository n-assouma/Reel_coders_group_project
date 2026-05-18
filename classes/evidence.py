### Author: Nael Karimou 5734316 start

import pygame

from .interactable_object import InteractableObject


class Evidence(InteractableObject):
    '''
    A piece of evidence that the player can collect and view
    in the evidence bag. Inherits from InteractableObject.
    '''

    def __init__(self, room_name: str, name: str, obj_data: dict) -> None:
        super().__init__(room_name, name, obj_data)
        self.collected = False
        self.visible = True
        # load sorting priority order for evidence bag 
        self.priority: int = obj_data['priority']
        self.is_key: bool = obj_data.get('is_key', False)

    def draw(
        self, surface: pygame.Surface, player_center: tuple[int, int]
    ) -> None:
        '''Draw evidence; also draws [E] prompt if near and not collected.'''
        if self.visible and not self.collected:
            super().draw(surface, player_center)

### Nael Karimou - 5734316 -end
