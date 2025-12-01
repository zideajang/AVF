
from enum import Enum,StrEnum
from typing import Protocol

from rich.console import Console

console = Console()

class TaskStatus(Enum):
    PENDING     = 0
    RUNNING     = 1
    COMPLETED   = 2
    FAILED      = 3

class TaskType(StrEnum):
    DEFAULT     = "default"
    MOVE        = "move"
    LAMBDA      = "lambda"
    DELAY       = "delay"
    NETWORK     = "network"

class TaskInterface(Protocol):

    def update(self,dt)->bool:
        pass

    def on_finish(self):
        pass

    
class BaseTask(TaskInterface):
    def __init__(self,name):
        self.name = name
        self.task_type = TaskType.DEFAULT
        self.status = TaskStatus.PENDING
        self.agent = None #依赖注入

    def start(self,agent):
        self.agent = agent
        self.status = TaskStatus.RUNNING
        console.print(f"{self.agent.name} start {self.name} task")

