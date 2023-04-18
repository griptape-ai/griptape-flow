from attr import define, field
from griptape.flow.drivers import MemoryDriver
from griptape.flow.memory import PipelineMemory


@define
class DiskMemoryDriver(MemoryDriver):
    file_path: str = field(default="griptape_memory.json", kw_only=True)

    def store(self, memory: PipelineMemory) -> None:
        with open(self.file_path, "w") as file:
            file.write(memory.to_json())

    def load(self) -> PipelineMemory:
        with open(self.file_path, "r") as file:
            memory = PipelineMemory.from_json(file.read())

            memory.driver = self

            return memory
