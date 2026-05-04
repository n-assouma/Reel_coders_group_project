# chief of police hint class for showing hints on HUD
# 5750779

import pygame
from settings import *


class ChiefOfPoliceHint:

    def __init__(self):
        # the message that gets shown in the panel
        self.current_hint = "Walk around with WASD. Get close to objects and press E."

        # font for the title at the top of the panel
        self.font_title = pygame.font.SysFont("Segoe UI,Arial", 15, bold=True)

        # font for the hint text in the body of the panel
        self.font_body = pygame.font.SysFont("Segoe UI,Arial", 14)

    def set_hint(self, text):
        # change the hint that the panel shows
        self.current_hint = text

    def draw(self, surface, x, y, w, h):
        # draw the chief of police panel inside the rectangle given to us

        # the rectangle that the panel sits in
        panel_rect = pygame.Rect(x, y, w, h)

        # dark background for the panel
        pygame.draw.rect(surface, COLOUR_HUD_PANEL, panel_rect, border_radius=6)

        # thin border around the panel
        pygame.draw.rect(surface, COLOUR_HUD_BORDER, panel_rect, 1, border_radius=6)

        # small coloured bar next to the title
        accent_bar = pygame.Rect(x + 10, y + 10, 3, 16)
        pygame.draw.rect(surface, COLOUR_TEXT_CHIEF, accent_bar)

        # the title text "CHIEF OF POLICE"
        title_surf = self.font_title.render("CHIEF OF POLICE", True, COLOUR_TEXT_CHIEF)
        surface.blit(title_surf, (x + 20, y + 9))

        # divider line under the title
        pygame.draw.line(surface, COLOUR_HUD_BORDER, (x + 10, y + 32), (x + w - 10, y + 32), 1)

        # draw the wrapped hint text below the divider line
        self.draw_wrapped(surface, self.current_hint, x + 12, y + 42, w - 24, COLOUR_TEXT)

    def draw_wrapped(self, surface, text, x, y, max_w, colour):
        # word wrap the text so it fits inside the panel
        # also respect newline characters in the hint

        # how tall one line of text is
        line_h = 19

        # current y position we are drawing at (we move it down as we go)
        text_y = y

        # split the text by newlines first so we get each paragraph
        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            # split the paragraph into single words
            words = paragraph.split(" ")

            # the line we are building up right now
            line = ""

            for word in words:
                # try adding the next word to the current line
                if line == "":
                    test = word
                else:
                    test = line + " " + word

                # check how wide the test line will be 
                width, height = self.font_body.size(test)

                if width <= max_w:
                    # the word still fits so keep it on this line
                    line = test
                else:
                    # the word does not fit, so draw what we have
                    rendered = self.font_body.render(line, True, colour)
                    surface.blit(rendered, (x, text_y))
                    text_y = text_y + line_h
                    # start the new line with this word
                    line = word

            # draw whatever is left on the last line of this paragraph
            if line != "":
                rendered = self.font_body.render(line, True, colour)
                surface.blit(rendered, (x, text_y))
                text_y = text_y + line_h
