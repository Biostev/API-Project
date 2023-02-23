from io import BytesIO

import pygame

from settings import *


class Map(pygame.sprite.Sprite):
    def __init__(self, group, position: tuple, init_buffer: bytes) -> None:
        super().__init__(group)
        self.image = pygame.image.load(BytesIO(init_buffer))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def make_map(self, buffer: bytes) -> None:
        self.image = pygame.image.load(BytesIO(buffer))
