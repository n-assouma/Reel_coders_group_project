### Nael Karimou - 5734316
import os
import sys

import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from settings import *


SUSPECTS = ['marcus', 'lena', 'victor']

KILLER = 'victor'
KEY_THRESHOLD = 3

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
        # store a reference to the main game screen
        self.screen = screen

        # instantiate an AccusationMenu
        self.accusation_menu = AccusationMenu(screen)

        # setting up the fontes to use
        self.font_title = pygame.font.SysFont(FONT, 48, bold=True)
        self.font_body = pygame.font.SysFont(FONT, 22)
        self.font_prompt = pygame.font.SysFont(FONT, 16)

    def run(self, key_count: int) -> None:
        '''Run the accusation menu and show the ending screen.'''

        # show the accusation menu and get the accused suspect name
        accused = self.accusation_menu.show()

        # determine the ending based on the accused and key_count
        if accused != KILLER:
            ending = 'C'
        elif key_count >= KEY_THRESHOLD:
            ending = 'A'
        else:
            ending = 'B'

        # show the ending screen 
        self._show(accused, ending) 


    def _show(self, accused: str, ending: str) -> None:
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
        # handle events when the Ending screen is on
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return


class AccusationMenu:
    '''Shows three suspect portraits and returns the name of the one clicked.'''

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.PORTRAIT_HEIGHT = 280
        self.PORTRAIT_GAP = 60

        # load the fonts for the text in the menu
        self.font_title = pygame.font.SysFont(FONT, 32, bold=True)
        self.font_name = pygame.font.SysFont(FONT, 20, bold=True)
        self.font_prompt = pygame.font.SysFont(FONT, 16)

        # load and prepare the portraits for display
        self._portraits = self._load_portraits()

    def _load_portraits(self) -> list[dict]:
        '''Load and scale each suspect portrait and calculate their positions.'''
        portraits = []

        # load the portrait sprites
        self._portraits_sprites = [
            pygame.image.load(
                os.path.join('assets', 'accusation_portrait', f'{suspect}.jpg')
            ).convert()
            for suspect in SUSPECTS
        ]

        # compute the total width of all portraits + gaps to center them
        total_width = sum(
            int(p.get_width() * self.PORTRAIT_HEIGHT / p.get_height())
            for p in self._portraits_sprites
        ) + self.PORTRAIT_GAP * (len(SUSPECTS) - 1)

        # starting  positions of the first portrait
        portrait_x = (SCREEN_WIDTH - total_width) // 2 
        portrait_y = int(SCREEN_HEIGHT * 0.25)

        # scale and position each portrait, and store the data in a list
        for suspect, sprite in zip(SUSPECTS, self._portraits_sprites):
            # scale the portrait to the fixed height and adjust width to maintain ratio
            scale = self.PORTRAIT_HEIGHT / sprite.get_height()
            scaled_width = int(sprite.get_width() * scale)
            sprite = pygame.transform.scale(sprite, (scaled_width, self.PORTRAIT_HEIGHT))

            #position the portrait
            rect = sprite.get_rect(topleft=(portrait_x, portrait_y))

            # store the portrait data 
            portraits.append({'name': suspect, 'sprite': sprite, 'rect': rect})

            # update x position for the next portrait
            portrait_x += scaled_width + self.PORTRAIT_GAP

        return portraits

    def show(self) -> str:
        '''
        Display the menu and block until a portrait is clicked.
        Returns the lowercase name of the accused suspect.
        '''
        hovered = None
        while True:
            for event in pygame.event.get():
                # if press the X to close the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # when mouse is moving
                if event.type == pygame.MOUSEMOTION:
                    hovered = self._get_hovered(event.pos)
                # when the player click somewhere on the screen
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = self._get_hovered(event.pos)
                    if clicked is not None:
                        return clicked
            # draw highlight around the portrait the mouse if on
            self._draw(hovered)


    def _get_hovered(self, pos: tuple[int, int]) -> str | None:
        '''Return the suspect name under the mouse position, or None.'''
        for portrait in self._portraits:
            if portrait['rect'].collidepoint(pos):
                return portrait['name']
        return None

    def _draw(self, hovered: str | None) -> None:
        self.screen.fill(COLOUR_HUD_BG)

        title = self.font_title.render("WHO IS THE CULPRIT?", True, COLOUR_HIGHLIGHT)
        title_pos = (
            SCREEN_WIDTH // 2 - title.get_width() // 2,
            int(SCREEN_HEIGHT * 0.1)
        )
        # Draw the title of the menu 'WHO IS THE CULPRIT?'
        self.screen.blit(title, title_pos)
    
        for portrait in self._portraits:
            sprite = portrait['sprite']
            rect = portrait['rect']
            name = portrait['name']

            # if the mouse is hovering on a portrait, draw a highlight around it
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
            
            # draw the portrait
            self.screen.blit(sprite, rect)

            # draw the name underneath it
            label = self.font_name.render(name.capitalize(), True, COLOUR_TEXT)
            label_pos = (rect.centerx - label.get_width() // 2, rect.bottom + 10)
            self.screen.blit(label, label_pos)

        # draw the indication for the player
        prompt = self.font_prompt.render(
            "Click a suspect to accuse them", True, COLOUR_TEXT_DIM
        )
        prompt_pos = (
            SCREEN_WIDTH // 2 - prompt.get_width() // 2,
            int(SCREEN_HEIGHT * 0.88)
        )
        self.screen.blit(prompt, prompt_pos)

        # update the display
        pygame.display.flip()


class EndingTracker:
    '''
    Tracks key evidence and event discoveries and determines the game ending.
    '''

    def __init__(self) -> None:
        self._key_count: int = 0

    def increment(self) -> None:
        '''Register one key evidence discovery.'''
        self._key_count += 1

    @property
    def key_count(self) -> int:
        '''Return the current number of key evidence discoveries.'''
        return self._key_count
    


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ending test")

    ending = EndingScreen(screen)
    tracker = EndingTracker()
    tracker.increment()
    tracker.increment()
    tracker.increment()

    number_of_key_evidence_and_event_discovored = tracker.key_count

    ending.run(number_of_key_evidence_and_event_discovored)

    pygame.quit()


### Nael Karimou - 5734316