### Nael Karimou - 5734316
import os
import sys

import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from settings import *


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

FONT = 'Segoe UI,Arial'


class EndingScreen:
    '''Displays the ending screen.'''

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        # setting up the fontes to use
        self.font_title = pygame.font.SysFont(FONT, 48, bold=True)
        self.font_body = pygame.font.SysFont(FONT, 22)
        self.font_prompt = pygame.font.SysFont(FONT, 16)

    def show(self, ending: str) -> None:
        '''
        Render the ending screen for the given ending key ('A', 'B', or 'C').
        The player should closes the window or press any key.
        '''
        data = ENDINGS[ending]
        self._draw(data['title'], data['body'])
        self._wait_for_input()

    def _draw(self, title: str, body: str) -> None:
        self.screen.fill(COLOUR_HUD_BG)

        # draw title of the ending
        title_surf = self.font_title.render(title, True, COLOUR_HIGHLIGHT)
        title_pos = (
                SCREEN_WIDTH // 2 - title_surf.get_width() // 2,
                int(SCREEN_HEIGHT * 0.25)
        )
        self.screen.blit(title_surf, title_pos)

        # draw body text
        current_line_pos = int(SCREEN_HEIGHT * 0.45)
        space = 8
        for line in body.split('\n'):
            line_surf = self.font_body.render(line, True, COLOUR_TEXT)
            line_pos = (SCREEN_WIDTH // 2 - line_surf.get_width() // 2, current_line_pos)
            self.screen.blit(line_surf, line_pos)
            current_line_pos += line_surf.get_height() + space

        # draw small prompt to close the window
        prompt = self.font_prompt.render("Press any key to exit", True, COLOUR_TEXT_DIM)
        prompt_pos = (
                SCREEN_WIDTH // 2 - prompt.get_width() // 2,
                int(SCREEN_HEIGHT * 0.85),
            )
        self.screen.blit( prompt, prompt_pos)

        #update diplay
        pygame.display.flip()

    def _wait_for_input(self) -> None:
        # handle events will the Ending screen is on
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return


SUSPECTS = ['marcus', 'lena', 'victor']

PORTRAIT_HEIGHT = 280
PORTRAIT_GAP = 60


class AccusationMenu:
    '''Shows three suspect portraits and returns the name of the one clicked.'''

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_title = pygame.font.SysFont(FONT, 32, bold=True)
        self.font_name = pygame.font.SysFont(FONT, 20, bold=True)
        self.font_prompt = pygame.font.SysFont(FONT, 16)
        self._portraits = self._load_portraits()

    def _load_portraits(self) -> list[dict]:
        '''Load and scale each suspect portrait, compute centered positions.'''
        portraits = []
        total_width = sum(
            int(p.get_width() * PORTRAIT_HEIGHT / p.get_height())
            for p in [
                pygame.image.load(
                    os.path.join('assets', 'accusation_portrait', f'{s}.jpg')
                ).convert()
                for s in SUSPECTS
            ]
        ) + PORTRAIT_GAP * (len(SUSPECTS) - 1)

        x = (SCREEN_WIDTH - total_width) // 2
        y = int(SCREEN_HEIGHT * 0.25)

        for suspect in SUSPECTS:
            path = os.path.join(
                'assets', 'accusation_portrait', f'{suspect}.jpg'
            )
            img = pygame.image.load(path).convert()
            scaled_w = int(img.get_width() * PORTRAIT_HEIGHT / img.get_height())
            img = pygame.transform.scale(img, (scaled_w, PORTRAIT_HEIGHT))
            rect = img.get_rect(topleft=(x, y))
            portraits.append({'name': suspect, 'image': img, 'rect': rect})
            x += scaled_w + PORTRAIT_GAP

        return portraits

    def show(self) -> str:
        '''Display the menu and block until a portrait is clicked.

        Returns the lowercase name of the accused suspect.
        '''
        hovered = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    hovered = self._get_hovered(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = self._get_hovered(event.pos)
                    if clicked is not None:
                        return clicked
            self._draw(hovered)

    def _get_hovered(self, pos: tuple[int, int]) -> str | None:
        '''Return the suspect name under the mouse position, or None.'''
        for portrait in self._portraits:
            if portrait['rect'].collidepoint(pos):
                return portrait['name']
        return None

    def _draw(self, hovered: str | None) -> None:
        self.screen.fill(COLOUR_HUD_BG)

        title = self.font_title.render("WHO DO YOU ACCUSE?", True, COLOUR_HIGHLIGHT)
        self.screen.blit(
            title,
            (SCREEN_WIDTH // 2 - title.get_width() // 2, int(SCREEN_HEIGHT * 0.1)),
        )

        for portrait in self._portraits:
            img = portrait['image']
            rect = portrait['rect']
            name = portrait['name']

            if name == hovered:
                highlight = pygame.Surface(
                    (rect.width + 6, rect.height + 6), pygame.SRCALPHA
                )
                highlight.fill((0, 0, 0, 0))
                pygame.draw.rect(
                    highlight, COLOUR_HIGHLIGHT,
                    (0, 0, rect.width + 6, rect.height + 6),
                    3, border_radius=4,
                )
                self.screen.blit(highlight, (rect.x - 3, rect.y - 3))

            self.screen.blit(img, rect)

            label = self.font_name.render(name.capitalize(), True, COLOUR_TEXT)
            self.screen.blit(
                label,
                (rect.centerx - label.get_width() // 2, rect.bottom + 10),
            )

        prompt = self.font_prompt.render(
            "Click a suspect to accuse them", True, COLOUR_TEXT_DIM
        )
        self.screen.blit(
            prompt,
            (
                SCREEN_WIDTH // 2 - prompt.get_width() // 2,
                int(SCREEN_HEIGHT * 0.88),
            ),
        )

        pygame.display.flip()


class EndingTracker:
    '''Tracks key evidence discoveries and determines the game ending.

    Call increment() each time the player find a key piece of evidence.
    Call get_ending(accused) when the player makes their accusation.
    '''

    KILLER = "victor"
    THRESHOLD = 3

    def __init__(self) -> None:
        self._key_count: int = 0

    def increment(self) -> None:
        '''Register one key evidence discovery.'''
        self._key_count += 1

    @property
    def key_count(self) -> int:
        '''Return the current number of key evidence discoveries.'''
        return self._key_count

    def get_ending(self, accused: str) -> str:
        '''Return the ending identifier based on who was accused.

        Args:
            accused: lowercase name of the accused suspect
                     ('victor', 'marcus', or 'lena')

        Returns:
            'A' - Justice served (correct accusation, enough evidence)
            'B' - Suspect escapes (correct accusation, not enough evidence)
            'C' - Wrong accusation
        '''
        # TODO: update _key_count by checking evidenc in the bag before triggering ending.
        if accused != self.KILLER:
            return 'C'
        if self._key_count >= self.THRESHOLD:
            return 'A'
        return 'B'


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ending test")

    tracker = EndingTracker()
    #tracker.increment()
    tracker.increment()
    tracker.increment()

    accused = AccusationMenu(screen).show()
    print(f"Accused: {accused}")

    ending = tracker.get_ending(accused)
    print(f"Ending: {ending}")

    EndingScreen(screen).show(ending)

    pygame.quit()


### Nael Karimou - 5734316