from griptape.flow.steps import PromptStep
from griptape.flow.structures import Pipeline
from griptape.flow.memory import BufferPipelineMemory
from tests.mocks.mock_driver import MockDriver


class TestBufferMemory:
    def test_after_run(self):
        memory = BufferPipelineMemory(buffer_size=2)

        pipeline = Pipeline(memory=memory, prompt_driver=MockDriver())

        pipeline.add_steps(
            PromptStep("test"),
            PromptStep("test"),
            PromptStep("test"),
            PromptStep("test")
        )

        pipeline.run()
        pipeline.run()

        assert len(pipeline.memory.runs) == 2
