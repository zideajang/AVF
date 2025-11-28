

from enum import StrEnum
from typing import Dict,Any,List,TypedDict
import pygame

default_animations_dict:Dict = {
            'up':{
                'row':8,
                'cols':9
            },
            'down':{
                'row':10,
                'cols':9
            },
            'left':{
                'row':9,
                'cols':9
            },
            'right':{
                'row':11,
                'cols':9
            },
            'up_idle':{
                'row':8,
                'cols':4
            },
            'down_idle':{
                'row':10,
                'cols':4
            },
            'left_idle':{
                'row':9,
                'cols':4
            },
            'right_idle':{
                'row':11,
                'cols':4
            }
            
        }

def create_animations(sheet:pygame.Surface,
                      animations_dict:Dict=default_animations_dict,
                      tile_size:int=64):
    animations = {}
    
    for animation in animations_dict:

        row = animations_dict[animation]['row']
        cols = animations_dict[animation]['cols']
        for col in range(cols):
            rect = pygame.Rect(
                col*tile_size,
                row* tile_size,
                tile_size,
                tile_size)
            image = sheet.subsurface(rect)
            if animation not in animations:
                animations[animation] = []
            animations[animation].append(image)

    return animations
class AgentState(StrEnum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    UP_IDLE = 'up_idle'
    DOWN_IDLE = 'down_idle'
    LEFT_IDLE = 'left_idle'
    RIGHT_IDLE = 'right_idle'

class BaseAgent(pygame.sprite.Sprite):

    def __init__(self,x,y,animations,obstacle_sprites=None):
        super().__init__()
        # 初始化状态
        self.status:AgentState=AgentState.DOWN_IDLE
        # color = "blue"
        # self.image = pygame.Surface((64,64))
        # self.image.fill(color)
        self.obstacle_sprites = obstacle_sprites

        self.sprite_hitbox_size = (-12,-12)

        self.animations = animations
        self.animation_speed = 0.15
        self.frame_index = 0
        self.image = animations[self.status][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.speed = 2
        
        self.target_pos = (x, y)
        self.moving_vector = pygame.math.Vector2(0, 0)
        self.is_moving = False

        self.hitbox = self.rect.inflate(
            self.sprite_hitbox_size[0],
            self.sprite_hitbox_size[1])

    def set_obstacle_sprites(self,obstacle_sprites):
        self.obstacle_sprites = obstacle_sprites
        

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]

    def set_target_pos(self,x,y):
        self.target_pos = (x, y)
        current_pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        target = pygame.math.Vector2(x, y)

        self.moving_vector = target - current_pos

        if self.moving_vector.length() > 0:
            self.moving_vector = self.moving_vector.normalize()
            self.is_moving = True
        else:
            self.is_moving = False
            self.moving_vector = pygame.math.Vector2(0, 0)

    def get_status(self):
        if self.is_moving:
            if abs(self.moving_vector.x) > abs(self.moving_vector.y):
                if self.moving_vector.x > 0:
                    self.status = AgentState.RIGHT
                else:
                    self.status = AgentState.LEFT
            else:
                if self.moving_vector.y > 0:
                    self.status = AgentState.DOWN
                else:
                    self.status = AgentState.UP

        else:
            if self.status in [AgentState.UP, AgentState.UP_IDLE]:
                self.status = AgentState.UP_IDLE
            elif self.status in [AgentState.DOWN, AgentState.DOWN_IDLE]:
                self.status = AgentState.DOWN_IDLE
            elif self.status in [AgentState.LEFT, AgentState.LEFT_IDLE]:
                self.status = AgentState.LEFT_IDLE
            elif self.status in [AgentState.RIGHT, AgentState.RIGHT_IDLE]:
                self.status = AgentState.RIGHT_IDLE
            else:
                self.status = AgentState.DOWN_IDLE



    def move(self):
        if not self.is_moving:
            # 如果 is_moving 为 False，则不执行任何移动操作
            self.direction = pygame.math.Vector2(0, 0)
            return

        # 1. 计算目标信息和减速速度
        current_center = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        target_center = pygame.math.Vector2(self.target_pos)
        distance_to_target = current_center.distance_to(target_center)
        
        # 实现平滑减速 (Ease-in): 实际速度取 self.speed 和剩余距离的较小值
        # 这确保了靠近目标时速度自然减慢
        actual_speed = min(self.speed, distance_to_target)

        # 2. 计算方向向量 (self.direction)
        if distance_to_target > 0:
            # 计算指向目标的单位向量 (normalized vector)
            self.direction = (target_center - current_center).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)
            
        # 3. 目标到达检测 (Stop condition)
        # 如果剩余距离小于等于本帧的移动距离 (actual_speed)
        if distance_to_target <= actual_speed:
            self.rect.center = self.target_pos
            self.hitbox.center = self.target_pos # 更新hitbox
            self.is_moving = False
            self.direction = pygame.math.Vector2(0, 0)
            return # 已经到达，停止执行后续的碰撞和移动

        # 4. 执行实际移动（基于 hitbox 和 direction/actual_speed）
        
        # 水平移动
        self.hitbox.x += self.direction.x * actual_speed
        self.collision('horizontal')

        # 垂直移动
        self.hitbox.y += self.direction.y * actual_speed
        self.collision('vertical')

        # 5. 更新可见矩形 (rect) 的位置
        self.rect.center = self.hitbox.center


    def collision(self, direction):
        # Collision logic as provided
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
    def update(self):
        self.get_status()
        self.move()
        self.animate()
        # self.rect.x += self.speed
        # self.rect.y += self.speed
    def draw(self):
        pass