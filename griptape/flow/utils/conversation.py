from __future__ import annotations
from typing import TYPE_CHECKING
from attr import define, field

if TYPE_CHECKING:
    from griptape.flow.memory import PipelineMemory


@define(frozen=True)
class Conversation:
    memory: PipelineMemory = field()

    def lines(self) -> list[str]:
        lines = []

        for run in self.memory.runs:
            lines.append(f"Q: {run.input}")
            lines.append(f"A: {run.output}")

        return lines

    def to_string(self) -> str:
        return str.join("\n", self.lines())
