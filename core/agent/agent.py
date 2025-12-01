from typing import Protocol

class Agent(Protocol):
    
    def talk_with(self,agent):
        pass