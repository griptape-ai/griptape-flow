from attr import define
from griptape.flow.drivers import PromptDriver
from griptape.flow.tokenizers import TiktokenTokenizer, BaseTokenizer
from griptape.flow.artifacts import TextOutput


@define
class MockValueDriver(PromptDriver):
    value: str
    model: str = "test-model"
    tokenizer: BaseTokenizer = TiktokenTokenizer()

    def try_run(self, **kwargs) -> TextOutput:
        return TextOutput(value=self.value, meta={})
