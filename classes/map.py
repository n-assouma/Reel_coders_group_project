### Amir H Javadi B 5717292
import os
import json
import pygame

from .room import Room
from .player import Player


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
            "marcus_house": {"rect": pygame.Rect(540, 42, 106, 88), "player_position": (589 - 15, 147 - 60)}
        }
        with open(os.path.join('data','rooms.json'), 'r') as f:
            self.room_data = json.load(f)
            # get rid of metadata
            self.room_data.pop('_meta', None)
        self.hud_map = Room('police_station', self.room_data['police_station']).objects['map_board']
        self.background = pygame.image.load(os.path.join('assets', 'map', 'map.png')).convert_alpha()
        self.background = pygame.transform.scale(self.background, (1200, 700))

    def name_maker(self, name):
        return name.replace("_", " ").upper()
    
    def get_hovered_room(self, mouse_posision):
        for name, rectangle in self.rooms_rect.items():
            if rectangle["rect"].collidepoint(mouse_posision):
                return name
        return None
    
    def draw(self, surface, current_room: Room, player_sprite=None):
        if self.is_open:
            surface.blit(self.background, (0, 0))
            mouse_posision = pygame.mouse.get_pos()
            hovered_room = self.get_hovered_room(mouse_posision)

            if player_sprite:
                    player_sprite = pygame.transform.scale(player_sprite, (30, 60))
                    surface.blit(player_sprite, self.rooms_rect[current_room.name]["player_position"] )
            
            if hovered_room:
                font = pygame.font.SysFont("Arial", 20)
                label = font.render(self.name_maker(hovered_room), True, (255, 255, 255))
                surface.blit(label, (self.rooms_rect[hovered_room]["rect"].x + self.rooms_rect[hovered_room]["rect"].width // 2 - label.get_width() // 2, self.rooms_rect[hovered_room]["rect"].y -40))

### Amir H Javadi B 5717292
                