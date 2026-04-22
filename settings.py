
# 5750779

# TODO: maybe move colours to a seperate file later

# screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# hud takes the bottom 28% of the screen
HUD_HEIGHT = int(SCREEN_HEIGHT * 0.28)
MAIN_SCREEN_HEIGHT = SCREEN_HEIGHT - HUD_HEIGHT



# colour for prompt tile border
COLOUR_HIGHLIGHT = (255, 230, 140)

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

# player speed
# TODO: make speed independent of FPS so that it is consistent across different machines. maybe use delta time?
PLAYER_SPEED = 1.5  # pixels per frame
INTERACTION_RADIUS = 55  # how close you need to be to press E

