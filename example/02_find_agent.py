import sys
import time
import pygame

from core.agent import RectAgent,BaseAgent,AgentGroup


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
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

            dt = pygame.time.Clock().tick(self.FPS)
            self.agents.update(dt)
            self.agents.draw(self.screen)
            pygame.display.flip()



if __name__ == "__main__":
    
    pygame.init()

    game = Game(name="find_target_demo")
    
    blue_rect_agent = RectAgent("alex",size=64,pos=(32,32),color=('blue'))
    yellow_rect_agent = RectAgent("tony",size=64,pos=(800,600),color=('yellow'))
    # 设置一个 target
    blue_rect_agent.set_target(yellow_rect_agent.rect.center)

    game.add_agent(blue_rect_agent)
    game.add_agent(yellow_rect_agent)
    game.run()

    pygame.quit()
