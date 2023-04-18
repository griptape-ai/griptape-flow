from tests.mocks.mock_driver import MockDriver
from griptape.flow.memory import PipelineMemory
from griptape.flow.steps import PromptStep
from griptape.flow.structures import Pipeline
from griptape.flow.utils import Conversation


class TestConversation:
    def test_lines(self):
        pipeline = Pipeline(prompt_driver=MockDriver(), memory=PipelineMemory())

        pipeline.add_steps(
            PromptStep("question 1")
        )

        pipeline.run()
        pipeline.run()

        lines = Conversation(pipeline.memory).lines()

        assert lines[0] == "Q: question 1"
        assert lines[1] == "A: mock output"
        assert lines[2] == "Q: question 1"
        assert lines[3] == "A: mock output"

    def test_to_string(self):
        pipeline = Pipeline(prompt_driver=MockDriver(), memory=PipelineMemory())

        pipeline.add_steps(
            PromptStep("question 1")
        )

        pipeline.run()

        string = Conversation(pipeline.memory).to_string()

        assert string == "Q: question 1\nA: mock output"
