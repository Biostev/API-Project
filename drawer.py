import pygame
from settings import *


class Drawer:
    def __init__(self, screen) -> None:
        self.screen = screen

    def draw_button(self, button) -> None:
        button_surface = pygame.Surface((button.size[0], button.size[1]))
        button_surface.fill(LIGHT_LIGHT_GREY)
        pygame.draw.rect(button_surface, button.color, (0, 0, button.size[0], button.size[1]), 5, button.rounding)
        font = pygame.font.SysFont('arial', 20)
        text_button = font.render(button.text, True, button.text_color)
        pos = text_button.get_rect(center=(button.size[0] // 2, button.size[1] // 2 - 1))
        button_surface.blit(text_button, pos)
        self.screen.blit(button_surface, (button.position[0], button.position[1]))

    def draw_input_box(self, input_box) -> None:
        font = pygame.font.Font(None, 25)
        txt_surface = font.render(input_box.text, True, input_box.text_color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.size = (width, input_box.size[1])
        input_box.input_rect = pygame.Rect(input_box.position[0], input_box.position[1],
                                           input_box.size[0], input_box.size[1])
        self.screen.blit(txt_surface, (input_box.position[0] + 5, input_box.position[1] + 5))
        pygame.draw.rect(self.screen, input_box.color, input_box.input_rect, 2)

    def draw_map(self, mapa):
        map_sprite.draw(self.screen)
