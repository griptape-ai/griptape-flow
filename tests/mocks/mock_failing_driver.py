from attr import define
from griptape.flow.drivers import BasePromptDriver
from griptape.flow.tokenizers import TiktokenTokenizer, BaseTokenizer
from griptape.flow.artifacts import TextOutput


@define
class MockFailingDriver(BasePromptDriver):
    max_failures: int
    current_attempt: int = 0
    model: str = "test-model"
    tokenizer: BaseTokenizer = TiktokenTokenizer()

    def try_run(self, **kwargs) -> TextOutput:
        if self.current_attempt < self.max_failures:
            self.current_attempt += 1

            raise Exception(f"failed attempt")
        else:
            return TextOutput("success")
