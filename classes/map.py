### Amir H Javadi B 5717292 - start
import os
import json
import pygame

from typing import Optional

from .room import Room
from .room_graph import RoomGraph


class Map:
    """Represents the interactive map UI in the game.

    Displays a full-screen map with clickable room regions, lock icons
    for locked rooms, the player's current position, and a hover label
    when the mouse is over a room.
    """

    def __init__(self):
        """Initialize the map UI, room rectangles, and assets."""
        self.is_open: bool = False

        # Each entry maps a room name to its clickable rect on the map
        # and the pixel position where the player sprite is drawn
        self.rooms_rect: dict[str, Room] = {
            "police_station": {
                "rect": pygame.Rect(506, 267, 169, 99),
                "player_position": (590 - 15, 403 - 60)
            },
            "elenas_office": {
                "rect": pygame.Rect(320, 467, 157, 123),
                "player_position": (505 - 15, 562 - 60)
            },
            "security_booth": {
                "rect": pygame.Rect(569, 439, 47, 62),
                "player_position": (591 - 15, 518 - 60)
            },
            "lenas_apartment": {
                "rect": pygame.Rect(910, 130, 131, 171),
                "player_position": (988 - 15, 325 - 60)
            },
            "victors_house": {
                "rect": pygame.Rect(84, 75, 193, 134),
                "player_position": (178 - 15, 313 - 60)
            },
            "faculty_dining_hall": {
                "rect": pygame.Rect(690, 486, 186, 109),
                "player_position": (782 - 15, 629 - 60)
            },
            "marcus_house": {
                "rect": pygame.Rect(540, 42, 106, 88),
                "player_position": (589 - 15, 147 - 60)
            }
        }

        # Load room data and strip internal metadata before use
        with open(os.path.join('data', 'rooms.json'), 'r', encoding='utf-8') as f:
            self.room_data = json.load(f)
            self.room_data.pop('_meta', None)

        # Grab the map board object from the police station room for the HUD
        self.hud_map = (
            Room('police_station', self.room_data['police_station'])
            .objects['map_board']
        )

        # Load and scale the map background image
        self.background = pygame.image.load(
            os.path.join('assets', 'map', 'map.png')
        ).convert_alpha()
        self.background = pygame.transform.scale(self.background, (1200, 700))

        # Load and scale the lock icon shown over locked rooms
        self.lock_sprite = pygame.image.load(
            os.path.join('assets', 'map', 'lock.png')
        ).convert_alpha()
        self.lock_sprite = pygame.transform.scale(self.lock_sprite, (60, 70))

    def name_maker(self, name: str) -> str:
        """Convert a snake_case room name to an uppercase display label.

        If the first word ends with 's', it is treated as a possessive name
        (e.g. 'elenas_office' -> "ELENA'S OFFICE").

        Args:
            name: The internal room name (e.g. 'elenas_office').

        Returns:
            The formatted name in uppercase (e.g. "ELENA'S OFFICE").
        """
        name_parts = name.split("_")
        if name_parts[0].endswith("s"):
            name_parts[0] = name_parts[0][:-1] + "'s"
        return " ".join(name_parts).upper()

    def get_hovered_room(self, mouse_position: tuple) -> Optional[str]:
        """Return the name of the room the mouse is currently over.

        Args:
            mouse_position: A (x, y) tuple of the current mouse position.

        Returns:
            The room name string if the mouse is over a room, otherwise None.
        """
        for name, rectangle in self.rooms_rect.items():
            if rectangle["rect"].collidepoint(mouse_position):
                return name
        return None

    def draw(self, surface, room_graph: RoomGraph,
             rooms_list: list[Room], current_room: Room,
             player_sprite=None) -> None:
        """Draw the map UI onto the given surface.

        Renders the map background, lock icons over locked rooms, the player
        sprite at the current room position, and a hover label for the room
        the mouse is pointing at.

        Args:
            surface: The pygame surface to draw onto.
            room_graph: The RoomGraph used to check if rooms are locked.
            rooms_list: List of all Room objects in the game.
            current_room: The Room the player is currently in.
            player_sprite: Optional pygame Surface for the player sprite.
        """
        if self.is_open:
            surface.blit(self.background, (0, 0))

            # Draw a lock icon centered above each locked room's position
            for room in rooms_list:
                if room_graph.is_room_locked(room):
                    pos = self.rooms_rect[room.name]["player_position"]
                    lock_x = pos[0] - self.lock_sprite.get_width() // 2 + 15
                    surface.blit(self.lock_sprite, (lock_x, pos[1]))

            mouse_position = pygame.mouse.get_pos()
            hovered_room = self.get_hovered_room(mouse_position)

            # Draw the player sprite at the current room's map position
            if player_sprite:
                player_sprite = pygame.transform.scale(player_sprite, (30, 60))
                surface.blit(
                    player_sprite,
                    self.rooms_rect[current_room.name]["player_position"]
                )

            # Draw a label above the room rect when the mouse hovers over it
            if hovered_room:
                font = pygame.font.SysFont("Arial", 20)
                label = font.render(
                    self.name_maker(hovered_room), True, (255, 255, 255)
                )
                rect = self.rooms_rect[hovered_room]["rect"]
                label_x = rect.x + rect.width // 2 - label.get_width() // 2
                label_y = rect.y - 40
                surface.blit(label, (label_x, label_y))
### Amir H Javadi B 5717292 - end
