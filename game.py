
# main game loop and drawing
# has the player, the room and the hud
# Andrei Sidorenko - 5750779
# Nael Karimou - 5734316

import json
import os
import pygame
import sys


from classes.interactable_object import Furniture, InteractableObject
from classes.room_graph import RoomGraph
from classes.evidence_bag import EvidenceBag
from classes.evidence import Evidence
from classes.room import Room
from classes.hud import HUD
from settings import *



class Game:
    ''''''
    def __init__(self) -> None:
        '''initialize pygame, create the window, load the player and the room.'''
        pygame.init()
        pygame.display.set_caption("The hollow witness")
        self.screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        print("pygame started")

        # Check if we really use it, if not we can remove it 
        self.font_title: pygame.font.Font = pygame.font.SysFont("Segoe UI,Arial", 18, bold=True)
        self.font_prompt: pygame.font.Font = pygame.font.SysFont("Segoe UI,Arial", 13, bold=True)

        # load the room data from the json file
        with open(os.path.join('data','rooms.json'), 'r') as f:
            room_data = json.load(f)
            # get rid of metadata
            room_data.pop('_meta', None)

        # create the rooms
        self.rooms = []
         # only load the first room for now
        self.rooms.append(Room('police_station', room_data['police_station']))
        self.rooms.append(Room('elenas_office', room_data['elenas_office']))
        
        # build the room graph
        # self.room_graph = RoomGraph(self.rooms)
        # set current room
        self.current_room: Room = self.rooms[0]

        self.evidence_bag: EvidenceBag = EvidenceBag()
        self.active_evidence = None
        self.hud: HUD = HUD(self.evidence_bag, self.current_room.objects['map_board'])
        self.running: bool = True
        print("game started")

        #TODO: DELETE THIS
        self.current_room = self.rooms[1]

    def run(self) -> None:
        '''game loop'''
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def _handle_events(self) -> None:
        '''
        handle window events and keyboard input
        '''
### Amir H Javadi B 5717292

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for num, evidence in enumerate(self.evidence_bag.items):
                        if evidence.rect.collidepoint(event.pos):
                            self.active_evidence = num
                    
                    if self.evidence_bag.rect.collidepoint(event.pos):
                        if self.evidence_bag.is_open:
                            self.evidence_bag.is_open = False
                        else:
                            self.evidence_bag.is_open = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.active_evidence = None
            if event.type == pygame.MOUSEMOTION:
                if self.active_evidence is not None:
                    self.evidence_bag.items[self.active_evidence].rect.move_ip(event.rel)

### Amir H Javadi B 5717292

            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_e:
                    self._try_interact()

    def _try_interact(self) -> None:
        player_center = self.current_room.player.get_center()
        '''check if the player is near any interactable objects and if so, interact with it.'''
        player_center = self.current_room.player.get_center()
        interactible_objects = filter(lambda obj: isinstance(obj, InteractableObject), self.current_room.objects.values()) 
        for obj in interactible_objects:
            if obj.is_player_near(player_center):
                if isinstance(obj, Evidence) and not obj.collected:
                    obj.collected = True
                    self.evidence_bag.add_evidence(obj)
                    self.evidence_bag.sort_by_priority()
                    self.hud.set_hint("You picked up: " + obj.name) 

                else:
                    print("[INTERACT] examined:", obj.name)
                    msg = "You examined the " + obj.name.lower() + ". (pickup/interaction logic coming from team)"
                    self.hud.set_hint(msg)
                return
            
    
    def _update(self) -> None:
        '''handle player movement and update hud hints'''
        keys = pygame.key.get_pressed()
        self.current_room.player.handle_movement(keys, self.current_room.collision_rects)

        player_center = self.current_room.player.get_center()

        # Set hud chief of police hint display to something. TODO: update with actual messages
        for obj_name in self.current_room.objects:
            obj = self.current_room.objects[obj_name]
            if type(obj) != Furniture:
                if obj.is_player_near(player_center):
                    self.hud.set_hint("That looks like a " + obj.name + ". Press E to examine it.")
                    return
            self.hud.set_hint("Walk around the station. Use WASD to move, E to interact.")

    def _draw(self) -> None:
        '''draw the current room, the player and the hud'''
        self.current_room.draw_background(self.screen)
        self.current_room.draw_room_objects(self.screen)
        self.hud.draw(self.screen, self.active_evidence)
        pygame.display.flip()

