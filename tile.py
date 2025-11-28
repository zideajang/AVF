import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, 
                 pos:tuple[int, int],
                 surf:pygame.Surface,
                 groups:pygame.sprite.AbstractGroup):
        super().__init__(groups)
        self.image:pygame.Surface = surf
        self.rect:pygame.Rect = self.image.get_rect(topleft=pos)
        self.hitbox:pygame.Rect = self.rect.inflate(0,-10)
        # self.hitbox.y += 5

    def draw_debug(self,surface: pygame.Surface):
        pygame.draw.rect(surface, 'red', self.hitbox, 2)
