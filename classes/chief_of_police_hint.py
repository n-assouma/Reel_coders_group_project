# chief of police hint class for showing hints on HUD
# 5750779

import json
import os
import pygame
from settings import *


# maps a dialogue speaker key to the title shown on the panel
SPEAKER_TITLES = {
    "chief": "CHIEF OF POLICE",
    "marcus": "MARCUS HALE",
    "lena": "LENA VOSS",
    "victor": "VICTOR OSEI",
    "waiter": "WAITER",
    "detective": "DETECTIVE ROWE"
}


# colour shown for the panel title depending on who is speaking
SPEAKER_COLOURS = {
    "chief": (120, 180, 230),       # blue (same as before)
    "detective": (230, 200, 100),   # warm yellow
    "marcus": (220, 110, 90),       # warm red
    "lena": (140, 200, 140),        # green
    "victor": (220, 180, 100),      # gold
    "waiter": (180, 170, 160)       # grey
}


class ChiefOfPoliceHint:

    def __init__(self):
        # default text shown when not near anything
        self.default_hint = "Walk around with WASD. Get close to objects and press E."
        # the message that gets shown in the panel right now
        self.current_hint = self.default_hint

        # default panel title (changes when an npc speaks)
        self.default_title = "CHIEF OF POLICE"
        self.current_title = self.default_title

        # colour the title is drawn in (changes per speaker)
        self.default_title_colour = COLOUR_TEXT_CHIEF
        self.current_title_colour = self.default_title_colour

        # true while a dialogue tree is active, so draw() shows the SPACE hint
        self.is_dialogue_active = False

        # whether the current dialogue node is the last one (changes hint text)
        self.is_dialogue_finished = False

        # countdown of frames during which the sticky hint stays visible
        # the proximity loop in game.py will skip overwriting while this > 0
        self.sticky_frames_left = 0

        # font for the title at the top of the panel
        self.font_title = pygame.font.SysFont("Arial", 17, bold=True)

        # font for the hint text in the body of the panel
        self.font_body = pygame.font.SysFont("Arial", 16)

        # chief lines loaded from json
        self.object_hints = {}
        self.room_unlocks_hints = {}
        # chief greeting lines for npcs (marcus, victor, waiter)
        self.npc_greetings = {}
        self.load_hints()

        # load all portraits used by the chief panel
        # the dictionary maps speaker key -> a loaded pygame surface
        # officer is the fallback used for chief, detective, and unknowns
        self.portrait_height = 140
        self.portraits = {}
        # table of files to try - speaker key, filename
        portrait_files = [
            ("officer", "Hud_officer.png"),
            ("marcus", "Hud_marcus.png"),
            ("victor", "Hud_victor.png"),
            ("lena", "Hud_lena.png"),
            ("waiter", "Hud_waiter.png"),
        ]
        # try to load each one - missing files are skipped
        for key, filename in portrait_files:
            path = os.path.join("assets", "hud", filename)
            try:
                raw = pygame.image.load(path).convert_alpha()
                # keep aspect ratio - scale by height
                original_w = raw.get_width()
                original_h = raw.get_height()
                ratio = self.portrait_height / original_h
                new_w = int(original_w * ratio)
                scaled = pygame.transform.smoothscale(raw, (new_w, self.portrait_height))
                self.portraits[key] = scaled
            except FileNotFoundError:
                print(filename + " not found, will use officer fallback")
            except pygame.error as err:
                print("could not load " + filename + ": " + str(err))

        # the sprite shown in the panel right now
        # starts as the officer (chief default)
        if "officer" in self.portraits:
            self.current_portrait = self.portraits["officer"]
        else:
            self.current_portrait = None

    def set_hint(self, text):
        # change the hint that the panel shows
        self.current_hint = text

    def set_speaker(self, speaker_name):
        # change the panel title to show who is speaking
        if speaker_name in SPEAKER_TITLES:
            self.current_title = SPEAKER_TITLES[speaker_name]
        else:
            # unknown speaker - just use the name in caps as fallback
            self.current_title = speaker_name.upper()

        # change the title colour to match the speaker
        if speaker_name in SPEAKER_COLOURS:
            self.current_title_colour = SPEAKER_COLOURS[speaker_name]
        else:
            # unknown speaker - fall back to the default chief colour
            self.current_title_colour = self.default_title_colour

        # change the portrait shown on the left of the panel
        # chief and detective both use the officer sprite
        # marcus, victor, lena, waiter use their own portraits if loaded
        if speaker_name in self.portraits:
            self.current_portrait = self.portraits[speaker_name]
        elif "officer" in self.portraits:
            # chief, detective, or any unknown speaker falls back to officer
            self.current_portrait = self.portraits["officer"]
        else:
            # nothing loaded at all
            self.current_portrait = None

    def set_dialogue_active(self, active):
        # tell the panel whether a dialogue is currently being shown
        # so it can draw the [SPACE] hint when needed
        self.is_dialogue_active = active

    def set_finished_hint(self, finished):
        # store whether the current dialogue node is the last one
        # so the hint reads "to close" instead of "to continue"
        self.is_dialogue_finished = finished

    def set_sticky_hint(self, text, frames):
        # show this hint and prevent it being overwritten for N frames
        self.current_hint = text
        self.sticky_frames_left = frames

    def tick_sticky(self):
        # called once per frame by Game._update
        # ticks the sticky countdown down by one
        if self.sticky_frames_left > 0:
            self.sticky_frames_left = self.sticky_frames_left - 1

    def is_sticky(self):
        # true if the panel is currently locked on a sticky message
        return self.sticky_frames_left > 0

    def get_room_unlocks_hint(self, room_name):
        # return the unlock hint string for a room or empty if missing
        if room_name in self.room_unlocks_hints:
            return self.room_unlocks_hints[room_name]
        return ""

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
        pygame.draw.rect(surface, self.current_title_colour, accent_bar)

        # the title text (changes based on current speaker)
        title_surf = self.font_title.render(self.current_title, True, self.current_title_colour)
        surface.blit(title_surf, (x + 20, y + 9))

        # divider line under the title
        pygame.draw.line(surface, COLOUR_HUD_BORDER, (x + 10, y + 32), (x + w - 10, y + 32), 1)

        # sprite on left, text on right
        sprite_padding = 10
        sprite_x = x + sprite_padding
        sprite_y = y + 25  # sits just under the divider line

        # only draw the sprite if one is set
        if self.current_portrait is not None:
            surface.blit(self.current_portrait, (sprite_x, sprite_y))
            # text starts to the right of the sprite, with a bit of space
            portrait_w = self.current_portrait.get_width()
            text_x = sprite_x + portrait_w + sprite_padding
        else:
            # no sprite, text uses the full panel width like before
            text_x = x + 12

        text_y = y + 42
        # leave room on the right edge for the map button drawn by the HUD
        map_button_reserved = 110
        text_max_w = (x + w) - text_x - 12 - map_button_reserved
        self.draw_wrapped(surface, self.current_hint, text_x, text_y, text_max_w, COLOUR_TEXT)

        # show a small [SPACE] hint at the bottom-right when a dialogue is active
        if self.is_dialogue_active:
            if self.is_dialogue_finished:
                hint_text = "[SPACE / E / ENTER] to close"
            else:
                hint_text = "[SPACE / E / ENTER] to continue"
            hint_surf = self.font_body.render(hint_text, True, COLOUR_TEXT_DIM)
            # offset the hint left of the map button so it stays visible
            hint_x = x + w - hint_surf.get_width() - 12 - 110
            hint_y = y + h - hint_surf.get_height() - 8
            surface.blit(hint_surf, (hint_x, hint_y))

    def draw_wrapped(self, surface, text, x, y, max_w, colour):
        # wrap text to fit, keep newlines

        # how tall one line of text is
        line_h = 22

        # current draw y (moves down each line)
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
            f = open(path, "r", encoding="utf-8")
            data = json.load(f)
            f.close()
        except FileNotFoundError:
            print("chief_hints.json not found at " + path)
            return
        except json.JSONDecodeError:
            print("chief_hints.json is not valid JSON")
            return

        # copy the sections we care about (skip _meta)
        if "object_hint" in data:
            self.object_hints = data["object_hint"]
        if "room_unlocks_hint" in data:
            self.room_unlocks_hints = data["room_unlocks_hint"]
        # copy npc greetings (marcus, victor, waiter)
        if "npc_greeting" in data:
            self.npc_greetings = data["npc_greeting"]

    def show_object_hint(self, object_name):
        # show chief's line, fallback if unknown
        # check npc greetings first - these describe the suspect / witness
        if object_name in self.npc_greetings:
            self.current_hint = self.npc_greetings[object_name]
        elif object_name in self.object_hints:
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
        # reset the title back to chief of police
        self.current_title = self.default_title
        # reset the title colour back to chief blue
        self.current_title_colour = self.default_title_colour
        # reset the portrait back to the officer
        if "officer" in self.portraits:
            self.current_portrait = self.portraits["officer"]
        else:
            self.current_portrait = None
