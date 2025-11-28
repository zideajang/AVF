import pygame
from src.agent import AgentState,BaseAgent,SpriteType

class UserProxyAgent(BaseAgent):
    def __init__(self, name, x, y, animations, obstacle_sprites=None):
        super().__init__(name, x, y, animations, obstacle_sprites)
        self.sprite_type = SpriteType.USER

        self.direction = pygame.math.Vector2()


    # 通过键盘来控制UserProxyAgent
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0


        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def draw(self,screen):
        screen.blit(self.image, self.hitbox)

    
    def move(self):
        
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def update(self):
        self.input()
        super().update()

