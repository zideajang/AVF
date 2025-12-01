import sys
import time
import pygame

from core.agent import RectAgent,BaseAgent,AgentGroup
from core.task import BaseTask,DelayTask,MoveToTask,LambdaTask

GRID_W = 30
GRID_H = 20
GRID_SIZE = 32

SCREEN_WIDTH    = GRID_SIZE * GRID_W
SCREEN_HEIGHT   = GRID_SIZE * GRID_H
BG_COLOR = 'lightgray'
FPS = 60



class Game:

    def __init__(self,name):
        
        self.name = name
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT


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
        for x in range(0, self.w, self.grid_size):
            # 线的起始点 (x, 0)，终止点 (x, screen_h)
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.h), self.grid_line_width)

        # 绘制水平线
        for y in range(0, self.h, self.grid_size):
            # 线的起始点 (0, y)，终止点 (screen_w, y)
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.w, y), self.grid_line_width)
    
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

            dt = pygame.time.Clock().tick(self.FPS)
            self.agents.update(dt)
            self.agents.draw(self.screen)
            pygame.display.flip()



if __name__ == "__main__":
    
    pygame.init()

    game = Game(name="find_multi_target")
    
    agent = RectAgent("alex",size=32,pos=(32,32),color=('blue'))
    agent.add_task(DelayTask(duration_sec=2.0, name="delay_task"))

    def change_agent_color(agent):
        agent.image.fill((125,125,0))
    agent.add_task(LambdaTask( name="change_agent_color",func=change_agent_color))
    agent.add_task(MoveToTask( name="change_agent_color",target_pos=pygame.Rect(600,200,32,32).center,stop_distance=32))
    def change_agent_color_again(agent):
        agent.image.fill((0,125,125))
    agent.add_task(LambdaTask( name="change_agent_color_again",func=change_agent_color_again))
    game.add_agent(agent)
    

    game.run()

    pygame.quit()
