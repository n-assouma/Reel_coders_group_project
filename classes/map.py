from .room import Room
from .player import Player
import os
import json
import pygame

class Map:
    def __init__(self):
        self.is_open: bool = False
        self.rooms_rect: dict[str, Room] = {
            "police_station": {"rect": pygame.Rect(506, 267, 169, 99), "player_position": (590 - 15, 403 - 60)},
            "elenas_office": {"rect": pygame.Rect(320, 467, 157, 123), "player_position": (505 - 15, 562 - 60)},
            "security_booth": {"rect": pygame.Rect(569, 439, 47, 62), "player_position": (591 - 15, 518 - 60)},
            "lenas_apartment": {"rect": pygame.Rect(910, 130, 131, 171), "player_position": (988 - 15, 325 - 60)},
            "victors_townhouse": {"rect": pygame.Rect(84, 75, 193, 134), "player_position": (178 - 15, 313 - 60)},
            "faculty_dining_hall": {"rect": pygame.Rect(690, 486, 186, 109), "player_position":(782 - 15, 629 - 60) },
            "marcuss_home": {"rect": pygame.Rect(540, 42, 106, 88), "player_position": (589 - 15, 147 - 60)}
        }
        with open(os.path.join('data','rooms.json'), 'r') as f:
            self.room_data = json.load(f)
            # get rid of metadata
            self.room_data.pop('_meta', None)
        self.hud_map = Room('police_station', self.room_data['police_station']).objects['map_board']
        self.background = pygame.image.load(os.path.join('assets', 'map', 'map.png')).convert_alpha()
        self.background = pygame.transform.scale(self.background, (1200, 700))

