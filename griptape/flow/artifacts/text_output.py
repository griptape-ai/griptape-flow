from typing import Optional
from attr import define, field
from griptape.flow.artifacts import StructureArtifact
from griptape.flow.tokenizers import TiktokenTokenizer, BaseTokenizer


@define(frozen=True)
class TextOutput(StructureArtifact):
    meta: Optional[any] = field(default=None)
    tokenizer: BaseTokenizer = field(default=TiktokenTokenizer(), kw_only=True)

    def token_count(self) -> Optional[int]:
        if isinstance(self.value, str):
            return self.tokenizer.token_count(self.value)
        else:
            return None
