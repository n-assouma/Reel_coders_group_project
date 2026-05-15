import os
import sys
import time

import pygame

# debugging: neccesary for settings imports to work when running this file directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from settings import (
    COLOUR_HUD_BG,
    COLOUR_HIGHLIGHT,
    COLOUR_TEXT,
    COLOUR_TEXT_DIM,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class LoadingBar:
    """Renders a progress bar on the loading screen."""

    def __init__(self) -> None:
        self.WIDTH = int(SCREEN_WIDTH * 0.5)   # bar cover half the screen width
        self.HEIGHT = 22
        self.X = (SCREEN_WIDTH - self.WIDTH) // 2   # centered horizontally
        self.Y = int(SCREEN_HEIGHT * 0.62)           # positioned in 1/3 of screen width
        self.FILL_COLOUR = (100, 160, 220)   # blue 
        self.BG_COLOUR = (30, 26, 36)        # dark 
        self.BORDER_COLOUR = (70, 55, 45)    # warm brown

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, progress: int) -> None:
        """Draw the bar at the given progress percentage (0-100)."""

        # draw the empty background of the bar
        pygame.draw.rect(
            screen,
            self.BG_COLOUR,
            (self.X, self.Y, self.WIDTH, self.HEIGHT),
            border_radius=6,
        )

        # compute and draw the filled portion of the bar
        fill_w = int(self.WIDTH * progress / 100)
        if fill_w > 0:
            filling_rect = (self.X, self.Y, fill_w, self.HEIGHT)
            pygame.draw.rect(
                screen,
                self.FILL_COLOUR,
                filling_rect,
                border_radius=6,
            )

        # draw the border 
        pygame.draw.rect(
            screen,
            self.BORDER_COLOUR,
            (self.X, self.Y, self.WIDTH, self.HEIGHT),
            2,            
            border_radius=6,
        )

        # compute the percentage  and center it below the bar
        percentage = font.render(f"{progress}%", True, COLOUR_TEXT)
        label_x = SCREEN_WIDTH // 2 - percentage.get_width() // 2
        label_y = self.Y + self.HEIGHT + 12   # 12px gap below the bar
        screen.blit(percentage, (label_x, label_y))


class LoadingScreen:
    """Displays a full-screen loading sequence before the game starts."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_title = pygame.font.SysFont("Segoe UI,Arial", 36, bold=True)
        self.font_small = pygame.font.SysFont("Segoe UI,Arial", 16)
        self.bar = LoadingBar()

    def update(self, progress: int) -> None:
        """Redraw the loading screen at the given progress (0-100).

        Call this after each loading step in game.pyto advance the bar.
        """
        for event in pygame.event.get():
            # allow the user to close mid-load.
            # This important because there is no other way to close 
            # the game window when tthe gam is loading
            if event.type == pygame.QUIT:   
                pygame.quit()
                sys.exit()
        self._draw(progress)

    def _draw(self, progress: int) -> None:

        # clear the screen each frame
        self.screen.fill(COLOUR_HUD_BG)   

        # draw the game title centered near the upper-middle of the screen
        title = self.font_title.render("THE HOLLOW WITNESS", True, COLOUR_HIGHLIGHT)
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        title_y = int(SCREEN_HEIGHT * 0.38)
        self.screen.blit(title, (title_x, title_y))

        # draw the "Loading..." subtitle centered below the title
        sub = self.font_small.render("Loading...", True, COLOUR_TEXT_DIM)
        sub_x = SCREEN_WIDTH // 2 - sub.get_width() // 2
        sub_y = int(SCREEN_HEIGHT * 0.50)
        self.screen.blit(sub, (sub_x, sub_y))

        self.bar.draw(self.screen, self.font_small, progress)
        # udpate the display after drawimg everything
        pygame.display.flip()   


# for debugging - should run this file directly to see how the screen loads
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    loader = LoadingScreen(screen)
    for step in (0, 25, 50, 75, 100):
        loader.update(step)
        time.sleep(2)
    pygame.quit()