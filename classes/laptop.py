### Amir H Javadi B 5717292

import pygame 
import os

from settings import *

class Laptop:

    PASSWORD_SIZE = 4
    PASSWORD = "7395" 

    def __init__(self):
        self.password_found: bool = False
        self.is_open: bool = False
        self.password_entered: str = ""

        self.laptop_image = pygame.image.load(os.path.join("assets", "laptop", "laptop.png") ).convert_alpha()
        self.laptop_image = pygame.transform.scale(self.laptop_image, (1200, 700))

        self.laptop_email_image = pygame.image.load(os.path.join("assets", "laptop", "laptop_email.png") ).convert_alpha()
        self.laptop_email_image = pygame.transform.scale(self.laptop_email_image, (1200, 700))

        self.font = pygame.font.SysFont("Segoe UI,Arial", 40, bold=True)
        self.text_surface = self.font.render("Enter Password", True, (255, 255, 255))

        self.text_w = self.text_surface.get_width() 
        self.text_h = self.text_surface.get_height() 
        self.text_x = (SCREEN_WIDTH - self.text_w) // 2
        self.text_y = (MAIN_SCREEN_HEIGHT - self.text_h) // 2

        self.box_lenght = 80
        self.pad = self.box_lenght // 2
        self.box_x = (SCREEN_WIDTH - (self.box_lenght * 4 + self.pad * 3)) // 2
        self.box_y = self.text_y + self.text_h + self.box_lenght // 2

        self.cross_bottom_rect = pygame.Rect(1095, 35, 56, 47)

        self.email_font = pygame.font.SysFont("Segoe UI,Arial", 20, bold=False)
        self.sender_text = self.email_font.render("From: victor.lockwood@gmail.com", True, (0, 0, 0))
        self.reciever_text = self.email_font.render("To: victor.lockwood@gmail.com", True, (0, 0, 0))
        self.subject_text = self.email_font.render("Subject: Reminder", True, (0, 0, 0))
        self.email_text = self.email_font.render("Elena knows about the grants....\n" \
        "She's threatening to go to the board\n" \
        "Handle this before tonight.", True, (0, 0, 0))

    def draw(self, surface):
        if self.is_open:
            if self.password_found:
                surface.blit(self.laptop_email_image, (0, 0))
                surface.blit(self.sender_text, (286 + 12, 170 + (30 - self.sender_text.get_height()) // 2))
                surface.blit(self.reciever_text, (286 + 12, 170 + 32.5 + (30 - self.reciever_text.get_height()) // 2))
                surface.blit(self.subject_text, (286 + 12, 170 + 65 + (30 - self.subject_text.get_height()) // 2))
                surface.blit(self.email_text, (286 + 12, 170 + 100 + (30 - self.subject_text.get_height()) // 2))
            else:
                surface.blit(self.laptop_image, (0, 0))
                surface.blit(self.text_surface, (self.text_x, self.text_y))
                for i in range(self.PASSWORD_SIZE):
                    box_rect = pygame.Rect(self.box_x + i * (self.box_lenght + self.pad), self.box_y, self.box_lenght, self.box_lenght)
                    pygame.draw.rect(surface, (255, 255, 255), box_rect, 2, border_radius=10)

                # displaying the entered password digits
        
                for num, digit in enumerate(self.password_entered):
                    digit_surface = self.font.render( digit, True, (255, 255, 255))
                    digit_w = digit_surface.get_width()
                    digit_h = digit_surface.get_height()
                    digit_x = self.box_x + num * (self.box_lenght + self.pad) + (self.box_lenght - digit_w) // 2
                    digit_y = self.box_y + (self.box_lenght - digit_h) // 2
                    surface.blit(digit_surface, (digit_x, digit_y))

### Amir H Javadi B 5717292