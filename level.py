import pygame

from agent import BaseAgent
from tile import Tile

class Level:
    def __init__(self,screen,tile_size,tmx_data):
        self.visible_sprites = pygame.sprite.Group()
        self.agents = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.features = ['funitures','decorations']
        self.tmx_data = tmx_data
        self.tile_size = tile_size
        self.screen = screen

        self.create_map()
    def add_agent(self,agent:BaseAgent):
        agent.set_obstacle_sprites(self.obstacle_sprites)
        self.agents.add(agent)
        

    def create_map(self):
        collision_layer = self.tmx_data.get_layer_by_name('collision')
        for x,y,surf in collision_layer.tiles():

            tile_surf = pygame.transform.scale(surf,(self.tile_size,self.tile_size))
            Tile(
                    pos=(x*self.tile_size,y*self.tile_size),
                    surf=tile_surf,
                    groups=self.obstacle_sprites
                )
        for feature in self.features:
            funiture_layer = self.tmx_data.get_layer_by_name(feature)
            for x,y,surf in funiture_layer.tiles():
                tile_surf = pygame.transform.scale(surf,(self.tile_size,self.tile_size))

                Tile(
                        pos=(x*self.tile_size,y*self.tile_size),
                        surf=tile_surf,
                        groups=[self.visible_sprites]
                    )
    


    def update(self,dt):
        for agent in self.agents:
            agent.update()
    def draw(self):
        self.visible_sprites.draw(self.screen)
        self.agents.draw(self.screen)
    def run(self,dt):
        self.update(dt)
        self.draw()
    