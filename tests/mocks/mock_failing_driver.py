from attr import define
from griptape.flow.drivers import PromptDriver
from griptape.flow.tokenizers import TiktokenTokenizer, Tokenizer
from griptape.flow.artifacts import TextOutput


@define
class MockFailingDriver(PromptDriver):
    max_failures: int
    current_attempt: int = 0
    model: str = "test-model"
    tokenizer: Tokenizer = TiktokenTokenizer()

    def try_run(self, **kwargs) -> TextOutput:
        if self.current_attempt < self.max_failures:
            self.current_attempt += 1

            raise Exception(f"failed attempt")
        else:
            return TextOutput("success")
