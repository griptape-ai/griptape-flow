from attr import define
from griptape.flow.drivers import PromptDriver
from griptape.flow.tokenizers import TiktokenTokenizer, BaseTokenizer
from griptape.flow.artifacts import TextOutput


@define
class MockDriver(PromptDriver):
    model: str = "test-model"
    tokenizer: BaseTokenizer = TiktokenTokenizer()

    def try_run(self, value: str) -> TextOutput:
        return TextOutput(value=f"mock output", meta={})
