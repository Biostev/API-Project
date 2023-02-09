import pygame
from settings import *


class Button:
    def __init__(self, enabled: bool,
                 position: tuple,
                 size: tuple,
                 color: tuple,
                 text_color: tuple,
                 text: str,
                 rounding: int) -> None:
        self.enabled = enabled
        self.position = position
        self.size = size
        self.color_const = color
        self.text_color_const = text_color
        self.color = color
        self.text_color = text_color
        self.text = text
        self.rounding = rounding

    def motion(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        x_mouse, y_mouse = mouse_pos
        if (self.position[0] <= x_mouse <= self.position[0] + self.size[0] and
                self.position[1] <= y_mouse <= self.position[1] + self.size[1]):
            self.color = DARK_GREY
            self.text_color = RED
        else:
            self.color = self.color_const
            self.text_color = self.text_color_const
        if (mouse_pressed[0] and self.position[0] <= x_mouse <= self.position[0] + self.size[0] and
                self.position[1] <= y_mouse <= self.position[1] + self.size[1]):
            return True
        return False

