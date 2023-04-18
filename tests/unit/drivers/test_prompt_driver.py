from tests.mocks.mock_failing_driver import MockFailingDriver
from griptape.flow.artifacts import ErrorOutput, TextOutput
from griptape.flow.steps import PromptStep
from griptape.flow.structures import Pipeline


class TestPromptDriver:
    def test_run_retries_success(self):
        driver = MockFailingDriver(max_failures=1, max_retries=1, retry_delay=0.01)
        pipeline = Pipeline(prompt_driver=driver)

        pipeline.add_step(
            PromptStep("test")
        )

        assert isinstance(pipeline.run().output, TextOutput)

    def test_run_retries_failure(self):
        driver = MockFailingDriver(max_failures=2, max_retries=1, retry_delay=0.01)
        pipeline = Pipeline(prompt_driver=driver)

        pipeline.add_step(
            PromptStep("test")
        )

        assert isinstance(pipeline.run().output, ErrorOutput)
