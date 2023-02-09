import pygame
from settings import *


class Map(pygame.sprite.Sprite):
    def __init__(self, group, position: tuple) -> None:
        super().__init__(group)
        self.image = pygame.image.load("map.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]

    def make_map(self) -> None:
        self.image = pygame.image.load("map.png")
