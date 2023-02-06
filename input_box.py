import pygame
from settings import *


class InputBox:
    def __init__(self, enabled: bool,
                 position: tuple,
                 size: tuple,
                 color: tuple,
                 text_color: tuple,
                 text: str,
                 background_text: str,
                 rounding: int) -> None:
        self.enabled = enabled
        self.position = position
        self.size = size
        self.color_const = color
        self.text_color_const = text_color
        self.color = color
        self.text_color = (179, 179, 179, 100)
        self.text = background_text
        self.background_text = background_text
        self.rounding = rounding
        self.input_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.active = False

    def motion(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = not self.active
                if self.text == self.background_text:
                    self.text = ""
            else:
                self.active = False
            self.color = DARK_DARK_GREY if self.active else self.color_const
            self.text_color = RED if self.active else self.text_color_const
            self.text = self.background_text if not self.active and not self.text else self.text
            if self.text == self.background_text:
                self.text_color = (179, 179, 179, 100)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = self.color_const
                    self.text_color = self.text_color_const
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode in "1234567890.,":
                        self.text += event.unicode
