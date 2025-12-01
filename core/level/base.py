import pygame

from core.agent import BaseAgent
from core.agent import AgentGroup,BaseAgent
from .tile import Tile
class Level:

    def __init__(self,name,
                 screen,
                 map,
                 grid_h,
                 grid_w,
                 grid_size=32):
        self.name = name
        self.map = map
        self.screen = screen

        self.grid_h = grid_h
        self.grid_w = grid_w
        self.grid_size = grid_size

        self.w = self.grid_w * self.grid_size
        self.h = self.grid_h * self.grid_size
        self.grid_color = (0,125,125)
        self.grid_line_width = 1

        self.agents = AgentGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.user:BaseAgent = None

        self.create_map()

    def draw_grid(self):
        for x in range(0, self.w, self.grid_size):
            # 线的起始点 (x, 0)，终止点 (x, screen_h)
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.h), self.grid_line_width)

        # 绘制水平线
        for y in range(0, self.h, self.grid_size):
            # 线的起始点 (0, y)，终止点 (screen_w, y)
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.w, y), self.grid_line_width)
    

    def create_map(self):
        title_surf = pygame.Surface((self.grid_size,self.grid_size))
        title_surf.fill((135,12,12) )
        for r in range(self.grid_h):
            for c in range(self.grid_w):
                if self.map[r][c] == 1:
                    Tile((c*self.grid_size,r*self.grid_size),title_surf,self.obstacle_sprites)
    def upate(self,dt):
        self.agents.update(dt)
    def draw(self):
        self.obstacle_sprites.draw(self.screen)
        self.agents.draw(self.screen)

    def add_agent(self,agent:BaseAgent):
        agent.set_obstacle_sprites(self.obstacle_sprites)
        self.agents.add(agent)
        

    def run(self,dt):
        self.upate(dt)
        self.draw()
    
if __name__ == "__main__":
    level_one = Level("office")