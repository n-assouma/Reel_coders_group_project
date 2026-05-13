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
from classes.laptop import Laptop
from classes.dialogue import load_dialogue_from_json, make_dialogue_key
from settings import *


# names of npc objects we can show evidence to
NPC_NAMES = ["marcus", "victor", "waiter"]


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
         # only load the first rooms for now
        self.rooms.append(Room('police_station', room_data['police_station']))
        self.rooms.append(Room('elenas_office', room_data['elenas_office']))
        self.rooms.append(Room('security_booth', room_data['security_booth'])) 
        self.rooms.append(Room('faculty_dining_hall', room_data['faculty_dining_hall']))
        self.rooms.append(Room('lenas_apartment', room_data['lenas_apartment']))
        self.rooms.append(Room('marcus_house', room_data['marcus_house']))
        self.rooms.append(Room('victors_house', room_data['victors_house']))


        # update the room connections to be actual room objects instead of strings. This is necessary for room graph to work
        self._update_room_connections_to_room_objects()

        # build the room graph
        self.room_graph = RoomGraph(self.rooms)
        self.room_graph.build_graph(self.rooms)
        # lock the edges that are supposed to be locked at the start of the game 
        self.room_graph.lock_room(self.rooms[3])
        self.room_graph.lock_room(self.rooms[4])
        self.room_graph.lock_room(self.rooms[6])

        # set current room
        self.current_room: Room = self.rooms[0]

        self.evidence_bag: EvidenceBag = EvidenceBag()
        self.active_evidence = None
        # the dialogue tree currently being shown, or None if no dialogue active
        self.active_dialogue = None
        # create the chief panel and map, then pass it into the HUD
        self.chief_hint = ChiefOfPoliceHint()
        self.map: Map = Map()
        self.laptop: Laptop = Laptop()
        self.hud: HUD = HUD(self.evidence_bag, self.chief_hint, self.map.hud_map)
          
        self.running: bool = True
        print("game started")

        # error handling for map navigation
        self.error_message = None
        self.error_time = None
        self.add_error_size = 0
        self.add_error_y = 0
        self.error_color = (255, 80, 80)

    def run(self) -> None:
        '''game loop'''
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
    
    ### Amir H Javadi B 5717292
    def _draw_error(self, surface, message: str = None, add_size: int = 0, add_y: int = 0, color: tuple = (255, 80, 80)) -> None:
        """Displaying error if any ahppened
            especially for the map navicgation,
            if the user wants to reach a room that there is a locked room in the middle of the path."""

        if message is not None:
            font = pygame.font.SysFont("Segoe UI,Arial", 22 + add_size, bold=True)
            padding  = 20
            text_surface = font.render(message, True, color)
            w = text_surface.get_width() + padding * 2
            h = text_surface.get_height() + padding * 2
            x = (SCREEN_WIDTH - w) // 2
            y = (MAIN_SCREEN_HEIGHT - h) // 2 - add_y

            box = pygame.Surface((w, h), pygame.SRCALPHA)
            box.fill((20, 0, 0, 200))
            surface.blit(box, (x, y))
            surface.blit(text_surface, (x + padding, y + padding))

    ### Amir H Javadi B 5717292

    def _handle_events(self) -> None:
        '''
        handle window events and keyboard input
        '''
### Amir H Javadi B 5717292

        for event in pygame.event.get():
            # if a dialogue is active, certain keys advance or close it
            if event.type == pygame.KEYDOWN:
                if self.active_dialogue is not None:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_e or event.key == pygame.K_RETURN:
                        # try to move to the next line in the dialogue
                        has_next = self.active_dialogue.advance()
                        if has_next:
                            # show the next line
                            next_node = self.active_dialogue.get_current()
                            self.chief_hint.set_speaker(next_node.speaker)
                            self.chief_hint.set_hint(next_node.text)
                        else:
                            # no more lines - close the dialogue
                            self.active_dialogue = None
                            self.chief_hint.show_default()
                    # eat the keypress either way so it does not trigger anything else
                    continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button

                    for num, evidence in enumerate(self.evidence_bag.items):
                        if evidence.rect.collidepoint(event.pos):
                            self.active_evidence = num
                    
                    #oppening and closing the evidence bag 

                    if self.evidence_bag.rect.collidepoint(event.pos):
                        if self.evidence_bag.is_open:
                            self.evidence_bag.is_open = False
                        else:
                            self.evidence_bag.is_open = True
                    
                    # closing the laptop by pressing the cross

                    if self.laptop.is_open:
                        if self.laptop.cross_bottom_rect.collidepoint(event.pos):
                            self.laptop.is_open = False
                            self.laptop.password_entered = ""

                    # oppening the map
                    
                    if self.hud.map_rect.collidepoint(event.pos):
                        self.map.is_open = True
                    
                    # hovering the room on the map --> shoeing the name of the room
                    # pressing on a room --> traveling to the room if it was available
                    # and displaying the error if not

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
                            else:
                                self.error_message = f"You need to unlock {self.map.name_maker(self.room_graph.route_with_blocker(self.current_room, distination_room).name)} first."
                                self.error_time = pygame.time.get_ticks()

            # removing an evidence from the evidence bag

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    if self.active_evidence is not None:
                        if self.evidence_bag.trash_can_image.get_rect(topleft=self.evidence_bag.trash_can_rect.topleft).collidepoint(event.pos):
                            item = self.evidence_bag.items[self.active_evidence]
                            self.evidence_bag.remove_evidence(item)
                            item.collected = False
                            item.rect = item.original_rect.copy()
                        else:
                            # check if the player dropped the evidence on an npc
                            self.try_start_dialogue(event.pos)

                        self.active_evidence = None
            
            # grabing and moving the evidences from the evidence bag 

            if event.type == pygame.MOUSEMOTION:
                if self.active_evidence is not None:
                    self.evidence_bag.items[self.active_evidence].rect.move_ip(event.rel)

            # typing the password on the laptop
            if event.type == pygame.KEYDOWN:
                if self.laptop.is_open and not self.laptop.password_found:
                    if event.unicode.isdigit():
                        if len(self.laptop.password_entered) < self.laptop.PASSWORD_SIZE:
                            self.laptop.password_entered += event.unicode
                    
                    elif event.key == pygame.K_BACKSPACE:
                        self.laptop.password_entered = self.laptop.password_entered[:-1]

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
                if obj.name == "map_board":
                    self.map.is_open = True
                if obj.name == "laptop":
                    self.laptop.is_open = True
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

    # try to start a dialogue when evidence was dropped at a screen position
    def try_start_dialogue(self, drop_pos):
        # only meaningful if there is a current room with objects
        if self.current_room is None:
            return

        # which evidence was being dragged
        item = self.evidence_bag.items[self.active_evidence]
        evidence_name = item.name

        # check every object in the room
        for obj_name in self.current_room.objects:
            obj = self.current_room.objects[obj_name]

            # only npcs trigger a dialogue
            if obj.name not in NPC_NAMES:
                continue

            # did the player drop the evidence on this npc?
            if not obj.rect.collidepoint(drop_pos):
                continue

            # build the lookup key and try to load the tree
            key = make_dialogue_key(evidence_name, obj.name)
            tree = load_dialogue_from_json(key)
            if tree is None:
                # no dialogue defined for this evidence + npc combo
                # let the player know with a chief line
                self.chief_hint.set_hint(
                    "They have nothing useful to say about this.")
                return

            # store the tree and show the first line
            self.active_dialogue = tree
            first_node = tree.get_current()
            # set the panel title to the speaker and show their text
            self.chief_hint.set_speaker(first_node.speaker)
            self.chief_hint.set_hint(first_node.text)

            # stop at the first matching npc
            return

    def _update(self) -> None:
        '''handle player movement and update hud hints'''
        # if a dialogue is active, freeze the rest of the update
        if self.active_dialogue is not None:
            return

        ### Amir H Javadi B 5717292

        if self.error_message and pygame.time.get_ticks() - self.error_time > 3000: # shoeing the error message for 3 seconds
            self.error_message = None
            self.error_time = None
            self.add_error_size = 0
            self.add_error_y = 0
            self.error_color = (255, 80, 80)
        
        if self.map.is_open:
            return 
        if self.laptop.is_open and not self.laptop.password_found:
            if len(self.laptop.password_entered) == self.laptop.PASSWORD_SIZE:
                if self.laptop.password_entered == self.laptop.PASSWORD:
                    self.error_message = "Password is correct!"
                    self.error_color = (0, 255, 0)
                    self.laptop.password_found = True
                else:
                    self.error_message = "Wrong password!"
                    self.laptop.password_entered = ""

                self.add_error_size = 20
                self.add_error_y = 175

                self.error_time = pygame.time.get_ticks()
            return
        
        # unlocking the rooms if the player has the required evidence in the bag 
        if self.evidence_bag.evidence_exists("dinner_invitation"):
            self.room_graph.unlock_room(self.rooms[3])
        if self.evidence_bag.evidence_exists("research_paper"):
            self.room_graph.unlock_room(self.rooms[4])
        if self.evidence_bag.evidence_exists("master_key_log"):
            self.room_graph.unlock_room(self.rooms[6])
        
        ### Amir H Javadi B 5717292

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
        self.laptop.draw(self.screen)
        self._draw_error(self.screen, self.error_message, self.add_error_size, self.add_error_y, self.error_color)
        
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