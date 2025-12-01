import pygame
from rich.console import Console

from .base_task import BaseTask,TaskInterface,TaskType,TaskStatus
console = Console()

class LambdaTask(BaseTask):

    def __init__(self, name,func):
        super().__init__(name)
        self.task_type = TaskType.LAMBDA
        self.func = func

    def start(self,agent):
                
        super().start(agent)
        if self.func:
            self.func(agent)
        self.status = TaskStatus.COMPLETED

    def update(self,dt):
        return True