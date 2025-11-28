import sys
import pygame
from pytmx.util_pygame import load_pygame
from src.agent import BaseAgent,create_animations
from src.user_proxy_agent import UserProxyAgent
from src.assistant_agent import AssistantAgent
from src.level import Level
from src.settings import *


class AgentOffice:
    def __init__(self,name):
        pygame.init()

        # 背景图片
        self.screen:pygame.surface.Surface = pygame.display.set_mode(
            (SCREEN_WIDTH,SCREEN_HEIGHT))
        self.orginal_bg = pygame.image.load(f"{ASSETS_ROOT_PATH}/tmx/{name}.png").convert()
        self.bg = pygame.transform.scale(self.orginal_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))


        # 资源
        tmx_data_path = f"{ASSETS_ROOT_PATH}/tmx/{name}.tmx"
        self.tmx_data = load_pygame(tmx_data_path)
        self.tile_size = TILE_SIZE

        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()

        # UserProxyAgent
        user_layer = self.tmx_data.get_layer_by_name("user")
        user_obj = user_layer[0]
        user_x,user_y = user_obj.x,user_obj.y
        user_name = "matthew"
        user_surface = pygame.image.load(f'./examples/office/graphics/character/user.png').convert_alpha()
        user_animations = create_animations(sheet=user_surface)
        user_grid_x = int(user_x*AGENT_SCALE)
        user_grid_y = int(user_y*AGENT_SCALE)

        user_proxy_agent = UserProxyAgent(name=user_name,
                               x=user_grid_x,
                               y=user_grid_y,
                              animations=user_animations)

        # Assistant Agents
        agents_layer = self.tmx_data.get_layer_by_name("agents")
        self.level = Level(self.screen,self.tile_size,self.tmx_data)
        self.level.add_user_proxy_agent(user_proxy_agent)
        for agent_obj in agents_layer:
            surface = pygame.image.load(f'./examples/office/graphics/character/{agent_obj.name}.png').convert_alpha()
            animations = create_animations(sheet=surface)
            x, y = agent_obj.x,agent_obj.y
            grid_x = int(x*AGENT_SCALE)
            grid_y = int(y*AGENT_SCALE)

            agent = AssistantAgent(name=agent_obj.name,x=grid_x,y=grid_y,
                              animations=animations)
            self.level.add_agent(agent)

    

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for sprite in self.level.agents.sprites():
                            if sprite.name == "alex":
                                print(sprite.name)
                                sprite.set_target_pos(x=10,y=10)
                    
            dt = self.clock.tick(FPS)
            self.screen.fill('lightgray')
            self.level.run(dt)
            # self.screen.blit(self.bg, (0, 0))
            
            pygame.display.update()
if __name__ == "__main__":
    game = AgentOffice("office")
    game.run()

