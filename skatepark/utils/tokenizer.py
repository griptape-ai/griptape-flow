from abc import ABC, abstractmethod
from typing import Optional


class Tokenizer(ABC):
    DEFAULT_STOP_SEQUENCE = "Observation:"

    model: str
    stop_sequence: str

    @property
    @abstractmethod
    def max_tokens(self) -> int:
        ...

    def tokens_left(self, text: str) -> int:
        diff = self.max_tokens - self.token_count(text)

        if diff > 0:
            return diff
        else:
            return 0

    def token_count(self, text: str) -> int:
        return len(self.encode(text))

    @abstractmethod
    def encode(self, text: str) -> list[int]:
        ...

    @abstractmethod
    def decode(self, tokens: list[int]) -> str:
        ...
