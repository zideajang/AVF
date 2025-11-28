

from enum import StrEnum
from typing import Dict,Any,List,TypedDict
import pygame
from src.settings import *

from abc import ABC,abstractmethod

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

class SpriteType(StrEnum):
    AGENT = "agent"
    USER = "user"


class BaseAgent(pygame.sprite.Sprite,ABC):

    def __init__(self,name,x,y,animations,obstacle_sprites=None):
        super().__init__()
        self.name = name
        # 初始化状态
        self.status:AgentState=AgentState.DOWN_IDLE
        # self.image = pygame.Surface((64,64))
        # self.image.fill(color)
        self.obstacle_sprites = obstacle_sprites
        self.sprite_hitbox_size = (-12,-12)


        self.animations = animations
        self.animation_speed = 0.15
        self.frame_index = 0
        self.image = animations[self.status][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = 2

        self.sprite_type = SpriteType.AGENT

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
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def get_status(self):
        pass

    def update(self):
        self.get_status()
        self.move()
        self.animate()
        # self.rect.x += self.speed
        # self.rect.y += self.speed
   