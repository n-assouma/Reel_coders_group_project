
# main game loop and drawing
# has the player, the room and the hud
# 5750779

import sys
import pygame
from settings import *
from classes.player import Player
from classes.room import Room, draw_furniture
from classes.hud import HUD
from classes.interactable_object import InteractableObject


class Game:
    "game window, main loop and render"

    def __init__(self) -> None:
        "py game start"
        pygame.init()
        pygame.display.set_caption("The hollow witness")
        self.screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        print("pygame started")

        self.font_title: pygame.font.Font = pygame.font.SysFont("Segoe UI,Arial", 18, bold=True)
        self.font_prompt: pygame.font.Font = pygame.font.SysFont("Segoe UI,Arial", 13, bold=True)

        start_x: int = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
        start_y: int = GAME_HEIGHT - PLAYER_HEIGHT - 60
        self.player: Player = Player(start_x, start_y)

        # demo room (AI)
        # TODO: load this from a json file later
        room: Room = Room("Police Station")
        room.add_furniture(100, 100, 80, 130)    # filing cabinet
        room.add_furniture(220, 160, 150, 55)    # typewriter desk
        room.add_furniture(430, 180, 220, 65)    # main desk
        room.add_furniture(100, 380, 170, 55)    # another desk

        lamp = InteractableObject(445, 155, 20, 28, "Desk lamp", kind="lamp")
        room.add_object(lamp)
        case_file = InteractableObject(500, 160, 38, 26, "Case file", clue_id="case_file", kind="paper")
        room.add_object(case_file)
        computer = InteractableObject(580, 160, 28, 24, "Computer", clue_id="computer", kind="computer")
        room.add_object(computer)
        board = InteractableObject(700, 120, 180, 100, "Suspects board", kind="board")
        room.add_object(board)
        typewriter = InteractableObject(125, 393, 28, 20, "Typewriter", kind="paper")
        room.add_object(typewriter)

        door_x: int = (SCREEN_WIDTH - 50) // 2
        door_y: int = GAME_HEIGHT - 70
        door = InteractableObject(door_x, door_y, 50, 60, "Elena's Office", kind="door")
        room.add_object(door)

        self.current_room: Room = room
        self.hud: HUD = HUD()
        self.running: bool = True
        print("game started")

    def run(self) -> None:
        "main loop"
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def _handle_events(self) -> None:
        "window and keyboard"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_e:
                    self._try_interact()

    def _try_interact(self) -> None:
        "radius of intercation"
        player_center = self.player.get_center()
        for obj in self.current_room.objects:
            if obj.is_player_near(player_center):
                print("[INTERACT] examined:", obj.name)
                msg = "You examined the " + obj.name.lower() + ". (pickup/interaction logic coming from team)"
                self.hud.set_hint(msg)
                return

    def _update(self) -> None:
        "movement and hud hints"
        keys = pygame.key.get_pressed()
        self.player.handle_movement(keys, self.current_room.walls)

        player_center = self.player.get_center()
        for obj in self.current_room.objects:
            if obj.is_player_near(player_center):
                self.hud.set_hint("That looks like a " + obj.name.lower() + ". Press E to examine it.")
                return
        self.hud.set_hint("Walk around the station. Use WASD to move, E to interact.")

    def _draw(self) -> None:
        "loop, Y sorted, hud"
        self.screen.fill(COLOUR_BG)
        self.current_room.draw_floor(self.screen, self.font_title)

        # collect every sprite with its y-sort key
        drawables: list[tuple[int, str, object]] = []

        # furniture (skip the first 4 walls because those are the room edges)
        for wall in self.current_room.walls[4:]:
            drawables.append((wall.bottom, "furniture", wall))

        # interactable objects — bundle the is_near flag so we only compute it once
        player_center = self.player.get_center()
        for obj in self.current_room.objects:
            is_near = obj.is_player_near(player_center)
            drawables.append((obj.rect.bottom, "object", (obj, is_near)))

        # player - derive bottom edge from center + half-height so this stays
        # correct even if the Player class doesn't expose a .rect attribute
        player_bottom: int = player_center[1] + PLAYER_HEIGHT // 2
        drawables.append((player_bottom, "player", self.player))

        # y-sort: ascending bottom-y → painter's algorithm for depth
        drawables.sort(key=lambda item: item[0])

        for _, kind, data in drawables:
            if kind == "furniture":
                draw_furniture(self.screen, data)
            elif kind == "object":
                obj, is_near = data
                obj.draw(self.screen, is_near, self.font_prompt)
            else:  # player
                data.draw(self.screen)

        # hud last so it covers everything
        self.hud.draw(self.screen)
        pygame.display.flip()
