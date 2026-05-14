### Nael Karimou - 5734316

import os
import sys

import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOUR_HUD_BG,
    COLOUR_HIGHLIGHT,
    COLOUR_TEXT,
    COLOUR_TEXT_DIM,
)


ENDINGS = {
    'A': {
        'title': 'CASE CLOSED',
        'body': (
            'Victor Osei found guilty. Confronted with the evidence,\n'
            'he confessed. Elena\'s family gets closure.\n'
            'Detective Rowe is commended.'
        ),
    },
    'B': {
        'title': 'CASE COLD',
        'body': (
            'Right suspect, insufficient evidence.\n'
            'Victor\'s solicitor blocked all charges.\n'
            'He shredded documents and fled the country.'
        ),
    },
    'C': {
        'title': 'INJUSTICE',
        'body': (
            'An innocent person was convicted.\n'
            'The real killer walked free.\n'
            'Six months later, new evidence surfaced — too late.'
        ),
    },
}


class EndingScreen:
    """Displays the ending screen and blocks until the player quits."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_title = pygame.font.SysFont("Segoe UI,Arial", 48, bold=True)
        self.font_body = pygame.font.SysFont("Segoe UI,Arial", 22)
        self.font_prompt = pygame.font.SysFont("Segoe UI,Arial", 16)

    def show(self, ending: str) -> None:
        """Render the ending screen for the given ending key ('A', 'B', or 'C').

        Blocks until the player closes the window or presses any key.
        """
        data = ENDINGS[ending]
        self._draw(data['title'], data['body'])
        self._wait_for_input()

    def _draw(self, title: str, body: str) -> None:
        self.screen.fill(COLOUR_HUD_BG)

        title_surf = self.font_title.render(title, True, COLOUR_HIGHLIGHT)
        self.screen.blit(
            title_surf,
            (
                SCREEN_WIDTH // 2 - title_surf.get_width() // 2,
                int(SCREEN_HEIGHT * 0.25),
            ),
        )

        y = int(SCREEN_HEIGHT * 0.45)
        for line in body.split('\n'):
            line_surf = self.font_body.render(line, True, COLOUR_TEXT)
            self.screen.blit(
                line_surf,
                (SCREEN_WIDTH // 2 - line_surf.get_width() // 2, y),
            )
            y += line_surf.get_height() + 8

        prompt = self.font_prompt.render(
            "Press any key to exit", True, COLOUR_TEXT_DIM
        )
        self.screen.blit(
            prompt,
            (
                SCREEN_WIDTH // 2 - prompt.get_width() // 2,
                int(SCREEN_HEIGHT * 0.85),
            ),
        )

        pygame.display.flip()

    def _wait_for_input(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return


class EndingTracker:
    """Tracks key evidence discoveries and determines the game ending.

    Call increment() each time the player find a key piece of evidence.
    Call get_ending(accused) when the player makes their accusation.
    """

    KILLER = "victor"
    THRESHOLD = 3

    def __init__(self) -> None:
        self._key_count: int = 0

    def increment(self) -> None:
        """Register one key evidence discovery."""
        self._key_count += 1

    @property
    def key_count(self) -> int:
        """Return the current number of key evidence discoveries."""
        return self._key_count

    def get_ending(self, accused: str) -> str:
        """Return the ending identifier based on who was accused.

        Args:
            accused: lowercase name of the accused suspect
                     ('victor', 'marcus', or 'lena')

        Returns:
            'A' - Justice served (correct accusation, enough evidence)
            'B' - Suspect escapes (correct accusation, not enough evidence)
            'C' - Wrong accusation
        """
        # TODO: update _key_count by checking evidenc in the bag before triggering ending.
        if accused != self.KILLER:
            return 'C'
        if self._key_count >= self.THRESHOLD:
            return 'A'
        return 'B'


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ending screen test")
    ending_screen = EndingScreen(screen)

    for ending in ('A', 'B', 'C'):
        print(f"Showing ending {ending}...")
        ending_screen.show(ending)

    pygame.quit()


### Nael Karimou - 5734316