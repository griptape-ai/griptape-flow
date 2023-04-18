from griptape.flow.summarizers import PromptDriverSummarizer
from griptape.flow.memory import SummaryPipelineMemory
from tests.mocks.mock_driver import MockDriver
from griptape.flow.steps import PromptStep
from griptape.flow.structures import Pipeline


class TestSummaryMemory:
    def test_unsummarized_steps(self):
        memory = SummaryPipelineMemory(offset=1, summarizer=PromptDriverSummarizer(driver=MockDriver()))

        pipeline = Pipeline(memory=memory, prompt_driver=MockDriver())

        pipeline.add_steps(
            PromptStep("test")
        )

        pipeline.run()
        pipeline.run()
        pipeline.run()
        pipeline.run()

        assert len(memory.unsummarized_runs()) == 1

    def test_after_run(self):
        memory = SummaryPipelineMemory(offset=1, summarizer=PromptDriverSummarizer(driver=MockDriver()))

        pipeline = Pipeline(memory=memory, prompt_driver=MockDriver())

        pipeline.add_steps(
            PromptStep("test")
        )

        pipeline.run()
        pipeline.run()
        pipeline.run()
        pipeline.run()

        assert memory.summary is not None
        assert memory.summary_index == 3
