import cohere
from attr import define, field
from griptape.flow.tokenizers import BaseTokenizer


@define(frozen=True)
class CohereTokenizer(BaseTokenizer):
    DEFAULT_MODEL = "xlarge"
    MAX_TOKENS = 2048

    model: str = field(default=DEFAULT_MODEL, kw_only=True)
    client: cohere.Client = field(kw_only=True)

    @property
    def max_tokens(self) -> int:
        return self.MAX_TOKENS

    def token_count(self, text: str) -> int:
        return len(self.encode(text))

    def encode(self, text: str) -> list[int]:
        return self.client.tokenize(text=text).tokens

    def decode(self, tokens: list[int]) -> str:
        return self.client.detokenize(tokens=tokens).text
