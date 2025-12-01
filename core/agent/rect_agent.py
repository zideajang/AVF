
import pygame
from enum import Enum
from .base_agent import BaseAgent,AgentType
from typing import Sequence

from rich.console import Console
from rich.text import Text

console = Console()

class TalkDirection(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    BOTTOM = 3 


class RectAgent(BaseAgent):
        
    def __init__(self,
                 name,
                 size,
                 pos,
                 color=(255,255,255),
                 speed=0.2 ):
        
        type = AgentType.RECT
        super().__init__(name, pos, type, speed)
        self.size = size

        self.color = color
        self.image = pygame.Surface((size,size))
        self.image.fill(self.color)

        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.current_target_pos = None
        self.targets = []

        self.obstacle_sprites = pygame.sprite.Group()
        
        self.sprite_hitbox_size = (-5,-5)
        self.hitbox = self.rect.inflate(
            self.sprite_hitbox_size[0],
            self.sprite_hitbox_size[1])


        self.offset = 10
        
        self.talk_direction:TalkDirection = TalkDirection.UP

    def set_obstacle_sprites(self,sprites):
        self.obstacle_sprites = sprites

    def set_target(self,target_pos:Sequence[float],is_insert=False):
        self.target_pos = pygame.math.Vector2(target_pos)
        if is_insert:
            self.targets.insert(0,target_pos)
        else:
            self.targets.append(target_pos)
    
    def collision(self,direction):
        # collision
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0 : 
                        self.hitbox.right = sprite.hitbox.left

                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                   
                    if self.direction.y > 0 : 
                        self.hitbox.bottom = sprite.hitbox.top

                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def set_paths(self,targets):
        self.targets.extend(targets)

    def move(self,dt):


        # self.hitbox.x += self.direction.x * speed
        # self.collision('horizontal')
        # self.hitbox.y += self.direction.y * speed
        # self.collision('vertical')

        # self.rect.center = self.hitbox.center

        if not self.is_moving or not self.current_target_pos:
            # text = Text()
            # text.append(f"{self.name} stop moving {self.is_moving},{self.current_target_pos}",style="cyan bold")
            # console.print(text)
            self.is_moving = False
            return
        
        # if self.target_pos:
        agent_vec = pygame.math.Vector2(self.rect.center)
        target_vec = pygame.math.Vector2(self.current_target_pos)

        distance = target_vec.distance_to(agent_vec)

        #  (abs(agent_vec.x - target_vec.x) - self.size >=0 
        #                         or abs(agent_vec.y - target_vec.y) - 10>=0): 

        self.direction = (target_vec - agent_vec).magnitude()
        if(self.direction > 0):
            self.direction = (target_vec - agent_vec).normalize()
        else:
            self.direction = pygame.math.Vector2()
        
        # text = Text()
        # text.append(f"{self.name} is moving...",style="blue bold")
        # text.append(f"direction:{round(self.direction,3)},")
        # text.append(f"distance:{round(distance,3)},")
        # text.append(f"target:{target_vec.x},{target_vec.y}")
        # text.append(f"distance_x:{round(abs(agent_vec.x - target_vec.x),3)},")
        # text.append(f"distance_y:{round(abs(agent_vec.y - target_vec.y),3)},")
        # console.print(text)

        delta_x = dt  * self.direction.x * self.speed.x
        delta_y = dt  * self.direction.y * self.speed.y


        # 先做判断，目标位置相对于当前位置的方向来确定 TalkDirection

        if distance >= self.size + self.offset:
            
            if self.talk_direction == TalkDirection.LEFT :
                if abs(delta_x) > abs(agent_vec.x - target_vec.x )- self.size:
                    self.hitbox.centerx = target_vec.x - self.size 

                else:
                    self.hitbox.centerx = int(self.hitbox.centerx + delta_x) 
                    self.collision('vertical')
                if abs(delta_y) > abs(agent_vec.y - target_vec.y):
                    self.hitbox.centery = target_vec.y
                else:
                    self.hitbox.centery = int(self.hitbox.centery + delta_y)
                    self.collision('vertical')

            elif self.talk_direction == TalkDirection.UP:
                if abs(delta_x) > abs(agent_vec.x - target_vec.x ):
                    self.hitbox.centerx = target_vec.x 
                else:
                    self.hitbox.centerx = int(self.hitbox.centerx + delta_x) 
                    self.collision('vertical')

                if abs(delta_y) > abs(agent_vec.y - target_vec.y) - self.size:
                    self.hitbox.centery = target_vec.y- self.size 
                else:
                    self.hitbox.centery = int(self.hitbox.centery + delta_y)
                    self.collision('vertical')
            self.rect.center = self.hitbox.center
        else:
            self.is_moving = False
            self.current_target_pos = None
            if self.talk_direction == TalkDirection.LEFT :
                self.rect.center = (int(target_vec.x - self.size), int(target_vec.y))
            elif self.talk_direction == TalkDirection.UP :
                self.rect.center = (int(target_vec.x ), int(target_vec.y - self.size))


            

        # move_distance = dt * self.speed

        # self.pos.x += self.direction.x * move_distance
        # self.pos.y += self.direction.y * move_distance

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_label(surface)
        self.draw_direction(surface)

    def update(self, dt,*args, **kwargs):

        # self.label = kwargs.get('message',self.name)

        self.update_tasks(dt)

        if len(self.targets) > 0 and not self.is_moving:
            # print(f"update{self.name},{self.is_moving=},{len(self.targets)}")
            self.current_target_pos = self.targets.pop()
            self.is_moving = True
        else:
            self.move(dt)
        # self.rect.x += self.speed.x * dt   
        # self.rect.y += self.speed.y * dt   