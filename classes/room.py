import os
import pygame

from .player import Player
from .interactable_object import *

class Room:
    def __init__(self, room_name: str, room_data: dict)-> None:
        self.name = room_name
        
        # load player at starting position
        self.player = Player(room_data['detective_rowe'])

        # load background
        path = os.path.join('assets',room_name, room_data['background']['path'])
        self.background = pygame.image.load(path).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, MAIN_SCREEN_HEIGHT))

        # keep track of drawable objects in the room for depth sorting and collision detection.
        self.room_objects = []

        # load furnitures and their data
        self.furnitures = {}
        for furniture_name in room_data['furnitures']:
            self.furnitures[furniture_name] = Furniture(room_name, furniture_name,
                                                         room_data[furniture_name])
            
            #add to room objects.
            self.room_objects.append(self.furnitures[furniture_name])

        # load interactible objects in the room
        self.interactable_objects = {}
        for obj_name in room_data['interactable_objects']:
            self.interactable_objects[obj_name] = InteractableObject(room_name, obj_name,
                                                                     room_data[obj_name])
            # add to drawable objects
            self.room_objects.append(self.interactable_objects[obj_name])

        # load evidences in the room
        self.evidences = {}
        for evidence_name in room_data['evidences']:
            self.evidences[evidence_name] = Evidence(room_name, evidence_name,
                                                                room_data[evidence_name])
            # add to drawable objects
            self.room_objects.append(self.evidences[evidence_name])


    def get_room_objects(self) -> list[Furniture]:
        '''
        Get the drawable objects in the room as a list.
        '''
        return self.room_objects

    def get_walkable_area(self) -> list[pygame.Rect]:
        '''
        Define the walkable area of the room as a list of pygame rectangles.
        This is used for border collision detection when the player moves around.
        It does not include the area occupied by furnitures.
        '''

    def draw_background(self, surface: pygame.Surface) -> None:
        '''
        Draw the background of the room onto the given surface.
        This should be called before drawing any furnitures or the player.
        '''
        surface.blit(self.background, (0, 0))

    def draw_room_object(self, surface: pygame.Surface, object_name: str) -> None:
        '''
        Draw a specific object in the room onto the given surface.
        This should be used when drawing the screen using depth sorting,
        so that objects are drawn in the correct order based on their y position.
        '''
        for obj in self.room_objects:
            if obj.name == object_name:
                if type(obj) == Furniture:
                    obj.draw(surface)
                else:
                    obj.draw(surface, self.player.get_center(), pygame.font.SysFont('Arial', 20))
                break
        else:
            print(f"Object '{object_name}' not found in room '{self.name}'")

    def __str__(self) -> str:
        return f"Room(name={self.name}, player_start={self.player_start}, furnitures={list(self.furnitures.keys())}, interactable_objects={list(self.interactable_objects.keys())}, evidences={list(self.evidences.keys())})"