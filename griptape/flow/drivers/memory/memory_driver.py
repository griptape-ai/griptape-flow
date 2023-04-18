from abc import ABC, abstractmethod
from griptape.flow.memory import PipelineMemory


class MemoryDriver(ABC):
    @abstractmethod
    def store(self, memory: PipelineMemory) -> None:
        ...

    @abstractmethod
    def load(self) -> PipelineMemory:
        ...
