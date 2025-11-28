import sys
import pygame
from pytmx.util_pygame import load_pygame
from agent import BaseAgent,create_animations
from level import Level

TILE_SIZE = 32
GRID_WIDTH = 30 
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE
AGENT_SCALE = 2

ASSETS_ROOT_PATH = "./examples/office/data/"

FPS = 60



class Game:
    def __init__(self,name):
        pygame.init()

        # 背景图片
        self.screen:pygame.surface.Surface = pygame.display.set_mode(
            (SCREEN_WIDTH,SCREEN_HEIGHT))
        self.orginal_bg = pygame.image.load(f"{ASSETS_ROOT_PATH}/tmx/{name}.png").convert()
        self.bg = pygame.transform.scale(self.orginal_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))

        # width = self.bg.get_width()
        # height = self.bg.get_height()
        # print(f"{width=},{height=}")
        # print(f"{SCREEN_WIDTH=},{SCREEN_HEIGHT=}")

        tmx_data_path = f"{ASSETS_ROOT_PATH}/tmx/{name}.tmx"
        self.tmx_data = load_pygame(tmx_data_path)
        
        self.tile_size = TILE_SIZE

        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()

        surface = pygame.image.load(f'./examples/office/graphics/character/alex.png').convert_alpha()
        animations = create_animations(sheet=surface)
        agent = BaseAgent(x=20,y=30,animations=animations)

        self.level = Level(self.screen,self.tile_size,self.tmx_data)
        self.level.add_agent(agent)
    

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.level.agents.sprites()[0].set_target_pos(x=480,y=320)
                    
            dt = self.clock.tick(FPS)
            self.screen.fill('lightgray')
            self.level.run(dt)
            # self.screen.blit(self.bg, (0, 0))
            
            pygame.display.update()
if __name__ == "__main__":
    game = Game("office")
    game.run()

