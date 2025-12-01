
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos,surf,groups):
        super().__init__(groups)
        self.image:pygame.Surface = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-5,-5)
        