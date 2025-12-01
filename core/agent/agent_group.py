import pygame


# AgengGroup(Group，业务逻辑)

class AgentGroup(pygame.sprite.Group):

    def draw(self, surface, bgsurf = None, special_flags = 0):
        for sprite in self.sprites():
            sprite.draw(surface)

    def update(self,dt:float, *args, **kwargs):
        for sprite in self.sprites():
            sprite.update(dt,*args, **kwargs)