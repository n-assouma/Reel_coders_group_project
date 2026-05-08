# chief of police hint class for showing hints on HUD
# 5750779

import json
import os
import pygame
from settings import *


class ChiefOfPoliceHint:

    def __init__(self):
        # default text shown when not near anything
        self.default_hint = "Walk around with WASD. Get close to objects and press E."
        # the message that gets shown in the panel right now
        self.current_hint = self.default_hint

        # font for the title at the top of the panel
        self.font_title = pygame.font.SysFont("Segoe UI,Arial", 15, bold=True)

        # font for the hint text in the body of the panel
        self.font_body = pygame.font.SysFont("Segoe UI,Arial", 14)

        # dictionaries that hold all the chief's lines from the json file
        self.object_hints = {}
        self.room_unlocks_hints = {}
        self.load_hints()

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

    def load_hints(self):
        # try to read the json file with all the chief hints
        path = os.path.join("data", "chief_hints.json")
        try:
            f = open(path, "r")
            data = json.load(f)
            f.close()
        except FileNotFoundError:
            print("chief_hints.json not found at " + path)
            return
        except json.JSONDecodeError:
            print("chief_hints.json is not valid JSON")
            return

        # copy the two sections we care about (skip _meta)
        if "object_hint" in data:
            self.object_hints = data["object_hint"]
        if "room_unlocks_hint" in data:
            self.room_unlocks_hints = data["room_unlocks_hint"]

    def show_object_hint(self, object_name):
        # show the chief's line for this object, or a generic message if there is no entry
        if object_name in self.object_hints:
            self.current_hint = self.object_hints[object_name]
        else:
            # fallback so unknown objects still show something
            self.current_hint = "That looks like a " + object_name.lower() + ". Press E to examine it."

    def show_room_unlocks_hint(self, room_name):
        # show the chief's line for unlocking this room
        if room_name in self.room_unlocks_hints:
            self.current_hint = self.room_unlocks_hints[room_name]

    def show_default(self):
        # reset to the default starting message
        self.current_hint = self.default_hint
