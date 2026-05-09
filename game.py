### Nael Karimou - 5734316

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
from classes.chief_of_police_hint import ChiefOfPoliceHint
from classes.map import Map
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
        self.rooms.append(Room('security_booth', room_data['security_booth'])) 
        self.rooms.append(Room('faculty_of_dining_hall', room_data['faculty_of_dining_hall']))

        # update the room connections to be actual room objects instead of strings. This is necessary for room graph to work
        self._update_room_connections_to_room_objects()

        # build the room graph
        self.room_graph = RoomGraph(self.rooms)
        self.room_graph.build_graph(self.rooms)
        # set current room
        self.current_room: Room = self.rooms[0]

        self.evidence_bag: EvidenceBag = EvidenceBag()
        self.active_evidence = None
        # create the chief panel and map, then pass it into the HUD
        self.chief_hint = ChiefOfPoliceHint()
        self.map: Map = Map()
        self.hud: HUD = HUD(self.evidence_bag, self.chief_hint, self.map.hud_map)
          
        self.running: bool = True
        print("game started")



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
                    
                    if self.hud.map_rect.collidepoint(event.pos):
                        self.map.is_open = True
                    
                    if self.map.is_open:
                        hovered_room = self.map.get_hovered_room(event.pos)
                        if hovered_room:
                            distination_room = None
                            for room in self.rooms:
                                if room.name == hovered_room:
                                    distination_room = room
                                    break
                            if self.room_graph.is_reachable(self.current_room, distination_room):
                                self.current_room = distination_room
                                self.map.is_open = False
                           
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

        # update the chief panel based on what (if anything) the player is near
        player_center = self.current_room.player.get_center()
        found = False
        for obj_name in self.current_room.objects:
            obj = self.current_room.objects[obj_name]
            if type(obj) != Furniture:
                if obj.is_player_near(player_center):
                    self.chief_hint.show_object_hint(obj.name)
                    found = True
                    break
        if not found:
            self.chief_hint.show_default()

    def _draw(self) -> None:
        '''draw the current room, the player and the hud'''
        self.current_room.draw_background(self.screen)
        self.current_room.draw_room_objects(self.screen)
        self.hud.draw(self.screen, self.active_evidence)
        self.map.draw(self.screen, self.current_room, self.current_room.player.front1_sprite)
        pygame.display.flip()

    def _update_room_connections_to_room_objects(self) -> None:
        for room in self.rooms:
            actual_room_connections = []
            for room_name in room.connections:
                for room_obj in self.rooms:
                    if room_obj.name == room_name:
                        actual_room_connections.append(room_obj)
                        break
            room.connections = actual_room_connections 
    



### Nael Karimou - 5734316