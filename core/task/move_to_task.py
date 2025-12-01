import pygame
from rich.console import Console

from .base_task import BaseTask,TaskInterface,TaskType,TaskStatus

console = Console()
class MoveToTask(BaseTask):
    def __init__(self, name,target_pos,stop_distance=5):
        super().__init__(name)
        self.task_type = TaskType
        self.target_pos = target_pos
        self.stop_distance = stop_distance


    def start(self,agent):
        super().start(agent)
        agent.set_target(self.target_pos)

    def update(self, dt):
        agent_pos = pygame.math.Vector2(self.agent.rect.center)
        target = pygame.math.Vector2(self.target_pos)

        distance = agent_pos.distance_to(target)

        if distance <= self.stop_distance or (not self.agent.is_moving and distance < self.agent.size):
            self.status = TaskStatus.COMPLETED
            return True
        return False
