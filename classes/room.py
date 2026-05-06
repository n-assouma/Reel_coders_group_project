### Author: Nael Karimou - 5734316


import os
import pygame

from .evidence import Evidence
from .player import Player
from .interactable_object import *

#The room should handle the collisin detection and y sorting
# a room should give oone method to draw the whole room. #TODO
class Room:
    '''
    A class representing a room with its own player and objects
    
    Methods:
    
    Attributes:
        Room.name : return current rroom name
        Room.player: return a reference to the player in the room
        Room.objects: return a dictionnary of all furniture in a room
        Room.connections: return a list of the names of the rooms that 
            are connected to the current room
        ...
    '''
    def __init__(self, room_name: str, room_data: dict)-> None:
        self.name = room_name

        # load the name of the rooms the current room is connected to.
        self._connections: list[str] = room_data['connections'] # load only the names of the rooms self is connected to
        
        # load player at starting position
        self.player = Player(room_data['detective_rowe'],
                            room_data['background']['walkable_area'])

        # load background
        path = os.path.join('assets',room_name, room_data['background']['path'])
        self.background = pygame.image.load(path).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, MAIN_SCREEN_HEIGHT))

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

        # get a list of object the player can collide with
        self._collision_rects = [
            self.objects[obj_name].collision_rect
            for obj_name in self.objects.keys()
            if self.objects[obj_name].collision == True
        ]

        # get a list of objects to sort by y position when drawing the room
        # for vertical sorting
        self._y_sort_lst: list[Player | Furniture | InteractableObject | Evidence] = []
        # add the player to the list
        self._y_sort_lst.append(self.player)

        # (re)defining furnitture y sorting position as it might not be properly set when the object is instantiated
        for obj_name in self.objects.keys():
            obj = self.objects[obj_name]
            if 'dropped_on' in room_data[obj_name]:
                obj_it_is_dropped_on = room_data[obj_name]['dropped_on']
                obj.y_sort_pos = 1 + self.objects[obj_it_is_dropped_on].rect.bottomleft[1] # adding 1 allow to draw it after the object it is dropped on

            # add furnitture to the list
            self._y_sort_lst.append(obj)


    @property
    def connections(self) -> list[str]:
        '''
        return a list of the names of the rooms that are connected to the current room
        '''
        return self._connections
    
    @connections.setter
    def connections(self, actual_connections: list[Room]) -> None:
        '''
        set the actual rooms the self is connected to. 
        This is necessary because of the wait RoomGraph setup the connections. 
        '''
        self._connections: list[Room] = actual_connections 
    
    @property
    def objects(self) -> dict:
        '''
        Get the all objects in the room.
        Return: a dictonnary where the key is the object name and the value
        is the object itself
        '''
        return self._objects #TODO: Define seperate function to load different types of objects
                             # if needed

    @property
    def collision_rects(self) -> pygame.Rect:
        '''
        return a list of object th plyer can collide with
        '''
        return self._collision_rects

    def draw_background(self, surface: pygame.Surface) -> None:
        '''
        Draw the background of the room onto the given surface.
        This should be called before drawing any furnitures or the player.
        '''
        surface.blit(self.background, (0, 0))

    def vert_sorted(self) -> list:
        '''
        return a list of all objects (including player) in the room sorted by their bottom left position for vertical sorting.
        This methods implements a custom bubble sort only use for our depth sorting
        '''
        for i in range(len(self._y_sort_lst)-1):
            if self._y_sort_lst[i].y_sort_pos > self._y_sort_lst[i+1].y_sort_pos:
                self._y_sort_lst[i], self._y_sort_lst[i+1] = self._y_sort_lst[i+1], self._y_sort_lst[i]
        return self._y_sort_lst

    def draw_room_objects(self, surface: pygame.Surface) -> None:
        '''
        Draw a specific object in the room onto the given surface.
        This should be used when drawing the screen using depth sorting,
        so that objects are drawn in the correct order based on their y position.
        '''
        sorted_objects = self.vert_sorted()
        for obj in sorted_objects:
            if type(obj) in (Player, Furniture):
                obj.draw(surface)

            elif type(obj) in (InteractableObject, Evidence):
                obj.draw(surface, self.player.get_center())
            
            else:
                print(f"Object '{type(obj)}' not found in room '{self.name}'")
        
    def __str__(self) -> str:
        return f"Room(name={self.name})"
    

### Nael Karimou - 5734316