import pygame
from src.agent import BaseAgent,AgentState

class AssistantAgent(BaseAgent):

    def __init__(self, name, x, y, animations, obstacle_sprites=None):
        super().__init__(name, x, y, animations, obstacle_sprites)

        self.target_pos = (x, y)

        self.target_pos = (x, y)
        self.moving_vector = pygame.math.Vector2(0, 0)
        self.is_moving = False

    def set_obstacle_sprites(self,obstacle_sprites):
        self.obstacle_sprites = obstacle_sprites

    def set_target_pos(self,x,y):
        
        self.target_pos = (x, y)
        print(f"{x=},{y=}")
        current_pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        target = pygame.math.Vector2(x, y)

        self.moving_vector = target - current_pos
        print(f"{self.moving_vector=},{current_pos=}")
        print(f"{self.moving_vector.length()}")

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