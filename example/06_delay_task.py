import sys
import time
import pygame

from core.agent import RectAgent,BaseAgent,AgentGroup
from core.task import DelayTask
GRID_W = 30
GRID_H = 20
GRID_SIZE = 32
UI_WIDTH = 256
SCREEN_WIDTH    = GRID_SIZE * GRID_W + UI_WIDTH
SCREEN_HEIGHT   = GRID_SIZE * GRID_H
BG_COLOR = 'lightgray'
FPS = 60



class Game:

    def __init__(self,name):
        
        self.name = name
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT

        self.main_screen_w = SCREEN_WIDTH - UI_WIDTH
        self.ui_screen_w = UI_WIDTH

        self.running = True
        # 创建窗口
        self.create_window()
        # Aents
        self.agents = AgentGroup()
        self.FPS = FPS

        self.grid_size = 32
        self.grid_color = (125,125,125)
        self.grid_line_width = 2

    def draw_grid(self):
        for x in range(0, self.main_screen_w, self.grid_size):
            # 线的起始点 (x, 0)，终止点 (x, screen_h)
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.h), self.grid_line_width)

        # 绘制水平线
        for y in range(0, self.h, self.grid_size):
            # 线的起始点 (0, y)，终止点 (screen_w, y)
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.main_screen_w, y), self.grid_line_width)

    def draw_ui(self):
        ui_bg_surf = pygame.Surface((self.ui_screen_w,self.h))
        ui_bg_surf.fill('blue')
        ui_rect = ui_bg_surf.get_rect()
        ui_rect.topleft = (self.main_screen_w,0)
        self.screen.blit(ui_bg_surf,ui_rect)

    def add_agent(self,agent:BaseAgent):
        self.agents.add(agent)
    
    def create_window(self):
        # 获取 surface
        self.screen = pygame.display.set_mode(
            (self.w,self.h)
        )
        pygame.display.set_caption(self.name)

    def run(self):

        start_time = time.time()
        delay_duration = 30
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

            elapsed_time = time.time() - start_time
            remaining_time = max(0, delay_duration - elapsed_time)
            if remaining_time <= 0:
                self.running = False

            self.screen.fill(BG_COLOR)
            self.draw_grid()
            self.draw_ui()

            dt = pygame.time.Clock().tick(self.FPS)
            self.agents.update(dt)
            self.agents.draw(self.screen)
            pygame.display.flip()



if __name__ == "__main__":
    
    pygame.init()

    game = Game(name="find_multi_target")
    
    agent = RectAgent("alex",size=32,pos=(32,32),color=('blue'))
    agent.add_task(DelayTask(duration_sec=2.0, name="delay_task"))
    # tony_agent = RectAgent("tony",size=32,pos=(800,32),color=('cyan'))
    # jerry_agent = RectAgent("jerry",size=32,pos=(800,480),color=('cyan'))
    
    # game.add_agent(tony_agent)
    # game.add_agent(jerry_agent)

    game.add_agent(agent)

    # agent.set_target(jerry_agent.rect.center)
    # agent.set_target(tony_agent.rect.center)
    

    game.run()

    pygame.quit()
