import cohere
from attr import define, field, Factory
from griptape.flow.artifacts import TextOutput
from griptape.flow.drivers import BasePromptDriver
from griptape.flow.tokenizers import CohereTokenizer


@define
class CoherePromptDriver(BasePromptDriver):
    api_key: str = field(kw_only=True)
    model: str = field(default=CohereTokenizer.DEFAULT_MODEL, kw_only=True)
    client: cohere.Client = field(
        default=Factory(lambda self: cohere.Client(self.api_key), takes_self=True), kw_only=True
    )
    tokenizer: CohereTokenizer = field(
        default=Factory(lambda self: CohereTokenizer(model=self.model, client=self.client), takes_self=True),
        kw_only=True
    )

    def try_run(self, value: any) -> TextOutput:
        result = self.client.generate(
            value,
            model=self.model,
            temperature=self.temperature,
            end_sequences=[self.tokenizer.stop_sequence, "Input:"],
            max_tokens=self.tokenizer.tokens_left(value)
        )

        if len(result.generations) == 1:
            generation = result.generations[0]

            return TextOutput(
                value=generation.text.strip(),
                meta=result.meta
            )
        else:
            raise Exception("Completion with more than one choice is not supported yet.")