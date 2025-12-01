import sys
import os
import time

from typing import List,Dict

import pygame

from core.agent import BaseAgent,AgentGroup,RectAgent
from core.level import Tile,Level

# constants

GRID_W = 20
GRID_H = 15
GRID_SIZE = 32
FPS= 60
SCREEN_WIDTH    = GRID_SIZE * GRID_W 
SCREEN_HEIGHT   = GRID_SIZE * GRID_H

layout = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,1,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]


class Game:
    def __init__(self,name:str,
                 w:int,h:int,
                 bg_color=(125,125,125)
                 ):
        pygame.init()
        self.name = name
        self.running = True
        self.h,self.w = h,w
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.w,self.h)
        )
        
        pygame.display.set_caption(self.name)

        self.levels = {}
    
    def add_level(self,level:Level):
        self.levels[level.name] = level

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick(FPS)
            
            self.screen.fill(self.bg_color)
            self.levels["level_one"].draw_grid()
            self.levels["level_one"].run(dt)
            pygame.display.update()



if __name__ == "__main__":
    game = Game(name="office",w=SCREEN_WIDTH,h=SCREEN_HEIGHT)

    agent = RectAgent("alex",size=32,pos=(0,0),color=('blue'))
    agent.set_target(pygame.Rect(18*GRID_SIZE,12*GRID_SIZE,GRID_SIZE,GRID_SIZE).center)

    level_one = Level(name="level_one",
                      screen=game.screen,
                      grid_h=GRID_H,
                      grid_w=GRID_W,
                      grid_size=GRID_SIZE,
                      map=layout)
    

    level_one.add_agent(agent)
    game.add_level(level_one)
    game.run()
