### Nael Karimou - 5734316 - start

import json
import os
import pygame
import sys


from classes.chief_of_police_hint import ChiefOfPoliceHint
from classes.dialogue import load_dialogue_from_json, make_dialogue_key
from classes.evidence import Evidence
from classes.evidence_bag import EvidenceBag
from classes.ending import EndingScreen, EndingTracker
from classes.hud import HUD
from classes.interactable_object import Furniture, InteractableObject
from classes.laptop import Laptop
from classes.loading_screen import LoadingScreen
from classes.map import Map
from classes.room import Room
from classes.room_graph import RoomGraph
from settings import *


# names of npc objects we can show evidence to
NPC_NAMES = ["marcus", "victor", "waiter", "lena"]


class Game:
    '''
    Main game controller for The Hollow Witness.

    Manages the game loop, all rooms, the player, evidence collection,
    NPC dialogues, the HUD, map navigation, and the laptop puzzle.
    Rooms are connected via a RoomGraph; some are locked until the player
    collects the required evidence. The game ends when the player interacts
    with the accusation board to trigger the ending screen.
    '''
    def __init__(self) -> None:
        '''initialize pygame, create the window, load the player and the room.'''
        pygame.init()
        pygame.display.set_caption("The hollow witness")
        self.screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        print("pygame started")

        # load loading screen - Aryan Naranath 5758224
        loader = LoadingScreen(self.screen)
        loader.update(0)

        # Check if we really use it, if not we can remove it 
        self.font_title: pygame.font.Font = pygame.font.SysFont("Segoe UI,Arial", 18, bold=True)
        self.font_prompt: pygame.font.Font = pygame.font.SysFont("Segoe UI,Arial", 13, bold=True)

        # load the room data from the json file
        with open(os.path.join('data','rooms.json'), 'r') as f:
            room_data = json.load(f)
            # get rid of metadata
            room_data.pop('_meta', None)

        #update loading screen - Aryan Naranath 5758224
        loader.update(10)

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

        #update loading screen - Aryan Naranath 5758224
        loader.update(50)


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

        # update loading screen - Aryan Naranath 5758224
        loader.update(65)

        self.evidence_bag: EvidenceBag = EvidenceBag()
        self.active_evidence = None
        # the dialogue tree currently being shown, or None if no dialogue active
        self.active_dialogue = None
        # rooms whose unlock hint has already been shown
        # so it does not spam the chief panel every frame
        self.shown_unlock_hints = set()
        # create the chief panel and map, then pass it into the HUD
        self.chief_hint = ChiefOfPoliceHint()
        self.map: Map = Map()
        self.laptop: Laptop = Laptop()
        self.hud: HUD = HUD(self.evidence_bag, self.chief_hint, self.map.hud_map)
        
        # update loading screen - Aryan Naranath 5758224
        loader.update(85)
          
        # error handling for map navigation
        self.error_message = None
        self.error_time = None
        self.add_error_size = 0
        self.add_error_y = 0
        self.error_color = (255, 80, 80)

        # set ending tracker to track key events accomplished
        self.tracker =  EndingTracker()

        # set ending  screen for when the player want to choose the murderer
        self.ending = EndingScreen(self.screen)
        
        #update loading screen - Aryan Naranath 5758224
        loader.update(100)
        
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

### Nael Karimou - 5734316 - end
    
### Amir H Javadi B 5717292 - start
    def _draw_error(
        self,
        surface,
        message: str = None,
        add_size: int = 0,
        add_y: int = 0,
        color: tuple = (255, 80, 80)
    ) -> None:
        """Display a semi-transparent error box on screen if a message is set.

        Used for map navigation errors when a locked room blocks the path,
        and for laptop password feedback.

        Args:
            surface: The pygame surface to draw onto.
            message: The error text to display, or None to draw nothing.
            add_size: Extra font size added to the default 22pt.
            add_y: Extra upward offset from the vertical center of the screen.
            color: RGB tuple for the text color.
        """
        if message is not None:
            font = pygame.font.SysFont("Segoe UI,Arial", 22 + add_size, bold=True)
            padding = 20
            text_surface = font.render(message, True, color)
            w = text_surface.get_width() + padding * 2
            h = text_surface.get_height() + padding * 2
            x = (SCREEN_WIDTH - w) // 2
            y = (MAIN_SCREEN_HEIGHT - h) // 2 - add_y

            # Semi-transparent dark red background behind the error text
            box = pygame.Surface((w, h), pygame.SRCALPHA)
            box.fill((20, 0, 0, 200))
            surface.blit(box, (x, y))
            surface.blit(text_surface, (x + padding, y + padding))

    def _handle_events(self) -> None:
        """Handle window events, keyboard input, and mouse interactions."""
### Amir H Javadi B 5717292 - end

 ### Andrei Sidorenko 5750779 - start
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
                            # update the hint depending on whether we just hit the last node
                            self.chief_hint.set_finished_hint(self.active_dialogue.is_finished())
                        else:
                            # no more lines - close the dialogue
                            self.active_dialogue = None
                            self.chief_hint.show_default()
                            # turn off the SPACE hint since dialogue is over
                            self.chief_hint.set_dialogue_active(False)
                    # eat the keypress either way so it does not trigger anything else
                    continue
 ### Andrei Sidorenko 5750779 - end
 ### Amir H Javadi B 5717292 - start

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button

                    # Pick up an evidence item if the bag is open and item is clicked
                    for num, evidence in enumerate(self.evidence_bag.items):
                        is_clicked = evidence.rect.collidepoint(event.pos)
                        if is_clicked and self.evidence_bag.is_open:
                            self.active_evidence = num

                    # Toggle the evidence bag open or closed
                    if self.evidence_bag.rect.collidepoint(event.pos):
                        self.evidence_bag.is_open = not self.evidence_bag.is_open

                    # Close the laptop when the X button is clicked
                    if self.laptop.is_open:
                        if self.laptop.cross_bottom_rect.collidepoint(event.pos):
                            self.laptop.is_open = False
                            self.laptop.password_entered = ""

                    # Open the map when the map icon in the HUD is clicked
                    if self.hud.map_rect.collidepoint(event.pos):
                        self.map.is_open = True

                    # Navigate to a room when clicked on the map
                    # Shows an error if a locked room blocks the path
                    if self.map.is_open:
                        hovered_room = self.map.get_hovered_room(event.pos)
                        if hovered_room:
                            destination_room = None
                            for room in self.rooms:
                                if room.name == hovered_room:
                                    destination_room = room
                                    break
                            if self.room_graph.is_reachable(
                                self.current_room, destination_room
                            ):
                                self.current_room = destination_room
                                self.map.is_open = False
                            else:
                                blocker = self.room_graph.route_with_blocker(
                                    self.current_room, destination_room
                                )
                                blocker_name = self.map.name_maker(blocker.name)
                                self.error_message = (
                                    f"You need to unlock {blocker_name} first."
                                )
                                self.error_time = pygame.time.get_ticks()

            # Drop evidence: remove it if dropped on trash can, or show dialogue
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    if self.active_evidence is not None:
                        trash_rect = self.evidence_bag.trash_can_image.get_rect(
                            topleft=self.evidence_bag.trash_can_rect.topleft
                        )
                        if trash_rect.collidepoint(event.pos):
                            item = self.evidence_bag.items[self.active_evidence]
                            self.evidence_bag.remove_evidence(item)
                            item.collected = False
                            item.rect = item.original_rect.copy()
                        else:
                            # Check if the player dropped the evidence on an NPC
                            self.try_start_dialogue(event.pos)

                        self.active_evidence = None

            # Drag the active evidence item with the mouse
            if event.type == pygame.MOUSEMOTION:
                if self.active_evidence is not None:
                    self.evidence_bag.items[self.active_evidence].rect.move_ip(
                        event.rel
                    )

            # Handle laptop password typing (digits and backspace)
            if event.type == pygame.KEYDOWN:
                if self.laptop.is_open and not self.laptop.password_found:
                    if event.unicode.isdigit():
                        if len(self.laptop.password_entered) < self.laptop.PASSWORD_SIZE:
                            self.laptop.password_entered += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        self.laptop.password_entered = self.laptop.password_entered[:-1]

### Amir H Javadi B 5717292 - end 

### Nael Karimou - 5734316 - start

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

                # if the player examine the accusation board
                if obj.name == 'accusation_board':
                    self.ending.run(self._update_tracker())
### Nael Karimou - 5734316 - end

### Andrei Sidorenko 5750779 - start
                # talking to the waiter starts a dialogue with his testimony
                if obj.name == "waiter":
                    self.start_npc_dialogue("waiter_testimony")
                    return
                # talking to marcus starts his introduction dialogue
                if obj.name == "marcus":
                    self.start_npc_dialogue("marcus_introduction")
                    return
                # talking to victor starts his introduction dialogue
                if obj.name == "victor":
                    self.start_npc_dialogue("victor_introduction")
                    return
                # talking to lena starts her introduction dialogue
                if obj.name == "lena":
                    self.start_npc_dialogue("lena_introduction")
                    return
                # pressing E on the keyboard tries to pull up the CCTV - which is dead
                if obj.name == "keyboard":
                    self.chief_hint.set_sticky_hint(
                        "Damn it. The cameras are dead. The recordings from last night were 'under maintenance'. Convenient.",
                        180)
                    return
### Andrei Sidorenko 5750779 - end

### Andrei Sidorenko 5750779 and Amir H Javadi B 5717292 -start
                if isinstance(obj, Evidence) and not obj.collected:
                    if self.evidence_bag.__len__() < self.evidence_bag.MAX_SIZE:
                        obj.collected = True
                        self.evidence_bag.add_evidence(obj)
                        self.evidence_bag.sort_by_priority()
                        self.hud.set_hint("You picked up: " + obj.name) 
                    else:
                        self.error_message = "Your bag is full!"
                        self.error_time = pygame.time.get_ticks()

                else:
                    print("[INTERACT] examined:", obj.name)
                    msg = "You examined the " + obj.name.lower() + ". (pickup/interaction logic coming from team)"
                    self.hud.set_hint(msg)
                return
            
### Andrei Sidorenko 5750779 and Amir H Javadi B 5717292 -end

### Andrei Sidorenko 5750779 - start

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
                # explicitly mark no dialogue active in case it was previously
                self.chief_hint.set_dialogue_active(False)
                return

            # store the tree and show the first line
            self.active_dialogue = tree
            # clear leftover sticky countdown so the panel does not
            # freeze on a stale message after the dialogue closes
            self.chief_hint.sticky_frames_left = 0
            first_node = tree.get_current()
            # set the panel title to the speaker and show their text
            self.chief_hint.set_speaker(first_node.speaker)
            self.chief_hint.set_hint(first_node.text)
            # tell the panel a dialogue is now active so it shows the SPACE hint
            self.chief_hint.set_dialogue_active(True)
            # tell the panel whether we are already at the last node
            self.chief_hint.set_finished_hint(tree.is_finished())

            # stop at the first matching npc
            return

    # start a dialogue tree from chief_hints.json by its key name
    # used when the player presses E next to an NPC
    def start_npc_dialogue(self, dialogue_key):
        # load the dialogue tree
        tree = load_dialogue_from_json(dialogue_key)
        if tree is None:
            # safety net - should never happen if json key matches
            self.chief_hint.set_hint("They have nothing to say right now.")
            self.chief_hint.set_dialogue_active(False)
            return

        # store the tree and show the first line
        self.active_dialogue = tree
        # clear leftover sticky countdown so the panel does not
        # freeze on a stale message after the dialogue closes
        self.chief_hint.sticky_frames_left = 0
        first_node = tree.get_current()
        # set the panel title to the speaker and show their text
        self.chief_hint.set_speaker(first_node.speaker)
        self.chief_hint.set_hint(first_node.text)
        # tell the panel a dialogue is now active so it shows the SPACE hint
        self.chief_hint.set_dialogue_active(True)
        # tell the panel whether we are already at the last node
        self.chief_hint.set_finished_hint(tree.is_finished())


    def _update(self) -> None:
        '''handle player movement and update hud hints'''
        # if a dialogue is active, freeze the rest of the update
        if self.active_dialogue is not None:
            return

        # tick the chief panel sticky countdown each frame
        self.chief_hint.tick_sticky()

### Andrei Sidorenko 5750779 - end

### Amir H Javadi B 5717292 - start

        # Clear the error message after 3 seconds
        elapsed = pygame.time.get_ticks() - self.error_time if self.error_time else 0
        if self.error_message and elapsed > 3000:
            self.error_message = None
            self.error_time = None
            self.add_error_size = 0
            self.add_error_y = 0
            self.error_color = (255, 80, 80)

        # Freeze game updates while the map is open
        if self.map.is_open:
            return

        # Handle laptop password validation when all digits are entered
        if self.laptop.is_open and not self.laptop.password_found:
            if len(self.laptop.password_entered) == self.laptop.PASSWORD_SIZE:
                if self.laptop.password_entered == self.laptop.PASSWORD:
                    self.error_message = "Password is correct!"
                    self.error_color = (0, 255, 0)
                    self.laptop.password_found = True
                else:
                    self.error_message = "Wrong password!"
                    self.laptop.password_entered = ""

                # Display feedback in the center of the laptop screen
                self.add_error_size = 20
                self.add_error_y = 175
                self.error_time = pygame.time.get_ticks()
            return

### Amir H Javadi B 5717292 - end 
### Andrei Sidorenko 5750779 and Amir H Javadi B 5717292 - start

        # unlocking the rooms if the player has the required evidence in the bag
        # also show a chief hint the first time each room becomes unlocked
        if self.evidence_bag.evidence_exists("dinner_invitation"):
            self.room_graph.unlock_room(self.rooms[3])
            room_name = self.rooms[3].name
            if room_name not in self.shown_unlock_hints:
                hint_text = self.chief_hint.get_room_unlocks_hint(room_name)
                # show for about 3 seconds at 60 fps
                self.chief_hint.set_sticky_hint(hint_text, 180)
                self.shown_unlock_hints.add(room_name)

        if self.evidence_bag.evidence_exists("research_paper"):
            self.room_graph.unlock_room(self.rooms[4])
            room_name = self.rooms[4].name
            if room_name not in self.shown_unlock_hints:
                hint_text = self.chief_hint.get_room_unlocks_hint(room_name)
                # show for about 3 seconds at 60 fps
                self.chief_hint.set_sticky_hint(hint_text, 180)
                self.shown_unlock_hints.add(room_name)

        if self.evidence_bag.evidence_exists("master_key_log"):
            self.room_graph.unlock_room(self.rooms[6])
            room_name = self.rooms[6].name
            if room_name not in self.shown_unlock_hints:
                hint_text = self.chief_hint.get_room_unlocks_hint(room_name)
                # show for about 3 seconds at 60 fps
                self.chief_hint.set_sticky_hint(hint_text, 180)
                self.shown_unlock_hints.add(room_name)
        
### Andrei Sidorenko 5750779 and Amir H Javadi B 5717292 - end

### Andrei Sidorenko 5750779 and Amir H Javadi B 5717292 and Nael Karimou 5734316 -start
        keys = pygame.key.get_pressed()
        self.current_room.player.handle_movement(keys, self.current_room.collision_rects)

        # only update the chief panel from proximity if no sticky hint is showing
        if not self.chief_hint.is_sticky():
            # update the chief panel based on what (if anything) the player is near
            player_center = self.current_room.player.get_center()
            found = False
            for obj_name in self.current_room.objects:
                obj = self.current_room.objects[obj_name]
                if type(obj) != Furniture:
                    # skip collected evidence so they don't trigger a hint
                    if obj.is_player_near(player_center) and not getattr(obj, 'collected', False):
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
        self.map.draw(self.screen, self.room_graph, self.rooms, self.current_room, self.current_room.player.front1_sprite)
        self.laptop.draw(self.screen)
        self._draw_error(self.screen, self.error_message, self.add_error_size, self.add_error_y, self.error_color)
        
        pygame.display.flip()

### Andrei Sidorenko 5750779 and Amir H Javadi B 5717292 and Nael Karimou 5734316 -start

### Nael Karimou - 5734316 - start
    def _update_room_connections_to_room_objects(self) -> None:
        '''
        Resolves room connections from name strings to Room object references.

        After rooms are loaded, each room's connections list contains room name
        strings. This method replaces those strings with the corresponding Room
        objects from self.rooms, so rooms can directly reference their neighbours.
        This is important for the room¬Graph to work
        '''
        for room in self.rooms:
            actual_room_connections = []
            for room_name in room.connections:
                for room_obj in self.rooms:
                    if room_obj.name == room_name:
                        actual_room_connections.append(room_obj)
                        break
            room.connections = actual_room_connections 

    def _update_tracker(self) -> int:
        '''
        This function update the state of the game tracker. It decide whether or not the 
        tracker should be incremented.
        Returns the number of key evidence and event found/completed by the player
        '''
        # Unlocking Victor computer is a key event
        if self.laptop.password_found:
            self.tracker.increment()

        # check how many key evidences are in the bag and update the tracker accordingly
        for evidence in self.evidence_bag.items:
            if evidence.is_key:
                self.tracker.increment()

        return self.tracker.key_count
     
### Nael Karimou - 5734316 -end
