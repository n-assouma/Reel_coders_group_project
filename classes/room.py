### Author: Nael Karimou - 5734316


import os
import pygame

from .player import Player
from .interactable_object import *

# TODO: Update this to room.json. I made think really harder for me 
#A room should own a player. TODO
#The room should handle the collisin detection and y sorting
# a room should give oone method to draw the whole room.
class Room:
    def __init__(self, room_name: str, room_data: dict)-> None:
        self.name = room_name
        
        # load player at starting position
        self.player = Player(room_data['detective_rowe'])

        # load background
        path = os.path.join('assets',room_name, room_data['background']['path'])
        self.background = pygame.image.load(path).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, MAIN_SCREEN_HEIGHT))

        # load background walkable area
        self._walkable_area = ... # TODO

        # load furniture, Interactable objects and evidences in the room with their name as a key
        self._objects = {}
        for obj_name in room_data['objects']:
            if obj_name not in self._objects:
                match room_data[obj_name]['class']:
                    case 'Furniture':
                        self._objects[obj_name] = Furniture(room_name, obj_name, room_data[obj_name])
                    case 'InteractableObject':
                        self._objects[obj_name] = InteractableObject(room_name, obj_name, room_data[obj_name])
                    case 'Evidence':
                        self._objects[obj_name] = Evidence(room_name, obj_name, room_data[obj_name])
                    case _:
                        # An error occured during loading, there is a typo in room.json. 
                        print(f"Object '{obj_name}' not found in room data for room '{room_name}'. Error may come from json file.")

            else:
                #if there is a duplicate of an object in rooms.json
                continue

        # get a list of obejct the player can collid with
        self._collision_rects = [
            self.objects[obj_name].collision_rect
            for obj_name in self.objects
            if self.objects[obj_name].collision == True
        ]

            

    @property
    def objects(self) -> dict:
        '''
        Get the all objects in the room.
        Return: a dictonnary with the following structure:
        {
            object_name: {
                object: the object itself
            },
            ...
        }
        '''
        return self._objects #TODO: Define seperate function to load different types of objects
                             # if needed

    @property
    def collision_rects(self):
        '''
        return a list of object th plyer can collide with
        '''
        return self._collision_rects
    

    # Dunno if we need that
    def get_walkable_area(self) -> pygame.Rect:
        '''
        Define the walkable area of the room as a list of pygame rectangles.
        This is used for border collision detection when the player moves around.
        It does not include the area occupied by furnitures.
        '''
        self._walkable_area

    def draw_background(self, surface: pygame.Surface) -> None:
        '''
        Draw the background of the room onto the given surface.
        This should be called before drawing any furnitures or the player.
        '''
        surface.blit(self.background, (0, 0))

    def depth_sorting(self) -> list:
        '''
        Get a list of all objects in the room sorted by their y position for depth sorting.
        This should be used when drawing the screen so that objects are drawn in the correct order.
        '''
        pass

    def draw_room_object(self, surface: pygame.Surface, object_name: str) -> None: # TODO: update this to use depth sorting
        '''
        Draw a specific object in the room onto the given surface.
        This should be used when drawing the screen using depth sorting,
        so that objects are drawn in the correct order based on their y position.
        '''
        #if the name of the object is valid
        if object_name in self.objects:
            if type(self.objects[object_name]) == Furniture:
                self.objects[object_name].draw(surface)

            elif type(self.objects[object_name]) in (InteractableObject, Evidence):
                self.objects[object_name].draw(surface, self.player.get_center())
        else:
            print(f"Object '{object_name}' not found in room '{self.name}'")
            

    def __str__(self) -> str:
        return f"Room(name={self.name})"
