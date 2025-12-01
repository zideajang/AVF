
from enum import StrEnum
from typing import Sequence
from collections import deque

from rich.console import Console

console = Console()

import pygame

FONT_NAME = 'arial'
FONT_SIZE = 16

DIRECTION_LINE_COLOR = (95,0,175) # 红色
DIRECTION_LINE_LENGTH = 50       # 线的长度（像素）
DIRECTION_LINE_WIDTH = 2         # 线的宽度

class AgentType:
    RECT = "rect"
    AGENET = "agent"
    USER = "user"



class BaseAgent(pygame.sprite.Sprite):

    def __init__(self,
                 name:str,
                 pos:Sequence[int],
                 type:AgentType, 
                 speed:float,
                 *groups):
        super().__init__(*groups)
        self.name = name
        self.type = type

        self.is_moving:bool = False

        self.speed = pygame.math.Vector2([speed,speed])
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2([0,0])



        self.task_queue = deque()
        self.current_task = None

        self.is_add_label = True
        self.label = self.name
        if self.is_add_label:
            self.font_name = FONT_NAME
            self.font_size = FONT_SIZE

            try:
                # 初始化 Pygame 字体
                self.font = pygame.font.SysFont(self.font_name, self.font_size)
            except:
                # 如果系统字体找不到，使用默认 None
                self.font = None

            

    def add_task(self,task,at_front=False):
        if at_front:
            self.task_queue.appendleft(task)
        else:
            self.task_queue.append(task)

    def update_tasks(self,dt):
        if not self.current_task:
            if self.task_queue:
                self.current_task = self.task_queue.popleft()
                self.current_task.start(self)
            else:
                return
            
        if self.current_task:
            is_finished = self.current_task.update(dt)
            if is_finished:
                self.current_task.on_finish()
                console.print(f"{self.name} completed {self.current_task.name}")
                self.current_task = None


    def draw_direction(self,screen):
        if self.is_moving and self.direction.length() > 0:
            
            # 线的起点是 Agent 的中心
            start_pos = pygame.math.Vector2(self.rect.center)
            
            # 计算线的终点: 起点 + (归一化方向向量 * 线的长度)
            end_pos = start_pos + (self.direction * DIRECTION_LINE_LENGTH)
            
            # 绘制线条
            pygame.draw.line(
                screen, 
                DIRECTION_LINE_COLOR, 
                start_pos, 
                end_pos, 
                DIRECTION_LINE_WIDTH
            )

    def draw_label(self,screen):
        if self.font:
            self.label_surface = self.font.render(self.label, True, (0, 0, 0)) # 文本颜色为白色
            self.label_rect = self.label_surface.get_rect()
            self.label_rect.centerx = self.rect.centerx
            self.label_rect.bottom =  self.rect.top - 8
            screen.blit(self.label_surface,self.label_rect)


        
         

    