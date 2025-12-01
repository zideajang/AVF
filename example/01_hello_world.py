import sys
import time
import random
import pygame

from core.agent import RectAgent,BaseAgent,AgentGroup

class Game:

    def __init__(self,name,w,h):
        self.name = name
        self.w = w
        self.h = h

        self.running = True
        # 初始化 pygame
        pygame.init()
        # 创建窗口
        self.create_window()
        # Aents
        self.agents = AgentGroup()
        self.FPS = 60
    
    def add_agent(self,agent:BaseAgent):
        self.agents.add(agent)
    
    def create_window(self):
        # 获取 surface
        self.screen = pygame.display.set_mode(
            (self.w,self.h)
        )

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

            self.screen.fill('lightgray')

            # text_content = f"{remaining_time:.1f}"
            # font, font style(bold,...) size

            # font = pygame.font.SysFont(None,128)
            # text_surface = font.render(text_content,True,(255,255,255))
            # text_rect = text_surface.get_rect(center=(self.w//2,self.h//2))
            # fill surface with color


            # target_pos = (800,600)
            # target_surf = pygame.Surface((64,64))
            # target_surf.fill('blue')
            # target_rect = target_surf.get_rect()
            # target_rect.topleft = target_pos

            # self.screen.blit(target_surf,target_rect)

            dt = pygame.time.Clock().tick(self.FPS)
            self.agents.update(dt)
            self.agents.draw(self.screen)

            
            # self.agent.update(dt)
            # self.agent.draw(self.screen)

            # self.screen.blit(text_surface,text_rect)
            # # surface
            pygame.display.flip()



if __name__ == "__main__":
    
    
    game = Game("hello world",w=1280,h=720)

    alex_rect_agent = RectAgent(name="alex",
                                size=64,
                                pos=(32,32),
                                color=('blue'))

    for i in range(10):
        pos = (random.randint(1,20) * 32,random.randint(1,20) * 32)
        color = ('yellow')
        rect_agent = RectAgent(f"Agent_{i}",size=64,pos=pos,color=color)
        game.add_agent(rect_agent)

    # SimpleAgent(name,size,pos,animation)
    tony_rect_agent = RectAgent("tony",
                                  size=64,
                                  pos=(800,600),
                                  color=('cyan'))
    game.add_agent(alex_rect_agent)
    game.add_agent(tony_rect_agent)
    game.run()

    pygame.quit()
