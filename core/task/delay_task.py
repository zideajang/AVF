from .base_task import BaseTask,TaskInterface,TaskType,TaskStatus

class DelayTask(BaseTask):

    def __init__(self, name,duration_sec):
        super().__init__(name)
        self.duration = duration_sec
        self.time = 0.0


    def update(self,dt):
        self.time += dt / 1000.0
        if self.time >= self.duration:
            self.status = TaskStatus.COMPLETED
            return True
        return False