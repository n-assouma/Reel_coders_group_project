
# 5750779

# TODO: maybe move colours to a seperate file later

# screen size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# hud takes the bottom 28% of the screen
HUD_HEIGHT = int(SCREEN_HEIGHT * 0.28)
GAME_HEIGHT = SCREEN_HEIGHT - HUD_HEIGHT

# colours (RGB)
# backgroubd layer
COLOUR_BG = (18, 16, 22)
COLOUR_FLOOR_LIGHT = (58, 46, 40)
COLOUR_FLOOR_DARK = (42, 33, 28)
COLOUR_FLOOR_LINE = (30, 24, 22)

# furniture
COLOUR_WOOD = (120, 78, 48)
COLOUR_WOOD_DARK = (70, 42, 26)
COLOUR_WOOD_HIGHLIGHT = (160, 110, 72)
# COLOUR_WOOD_OLD = (100, 60, 40)  # i changed this but i keep it just in case

# player colours
COLOUR_PLAYER_BODY = (130, 90, 60)
COLOUR_PLAYER_DARK = (80, 50, 30)
COLOUR_PLAYER_HEAD = (220, 180, 140)
COLOUR_PLAYER_HAIR = (50, 35, 25)

# interactive objects
COLOUR_OBJECT = (200, 170, 90)
COLOUR_OBJECT_DARK = (140, 110, 50)
COLOUR_HIGHLIGHT = (255, 230, 140)

# doors
COLOUR_DOOR = (150, 95, 55)
COLOUR_DOOR_DARK = (90, 55, 30)

# hud
COLOUR_HUD_BG = (14, 12, 18)
COLOUR_HUD_PANEL = (24, 20, 28)
COLOUR_HUD_BORDER = (70, 55, 45)

# text colours
COLOUR_TEXT = (225, 215, 195)
COLOUR_TEXT_DIM = (130, 115, 100)
COLOUR_TEXT_CHIEF = (120, 180, 230)
COLOUR_TEXT_EVIDENCE = (230, 185, 100)
COLOUR_TEXT_NOTEPAD = (150, 200, 140)

# player size/speed
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 32
PLAYER_SPEED = 3
INTERACTION_RADIUS = 55  # how close you need to be to press E

# floor tile
TILE_SIZE = 48

# paths (not using these yet but i think we need them)
DATA_DIR = "data"
ROOMS_JSON = "data/rooms.json"
CLUES_JSON = "data/clues.json"
CHIEF_HINTS_JSON = "data/chief_hints.json"
