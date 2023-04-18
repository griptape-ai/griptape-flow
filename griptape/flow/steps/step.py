from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Optional
from attr import define, field, Factory
from griptape.flow.artifacts import ErrorOutput

if TYPE_CHECKING:
    from griptape.flow.artifacts import TextOutput, StructureArtifact
    from griptape.flow.steps import Step
    from griptape.flow.structures import Structure


@define
class Step(ABC):
    class State(Enum):
        PENDING = 1
        EXECUTING = 2
        FINISHED = 3

    id: str = field(default=Factory(lambda: uuid.uuid4().hex), kw_only=True)
    state: State = field(default=State.PENDING, kw_only=True)
    type: str = field(default=Factory(lambda self: self.__class__.__name__, takes_self=True), kw_only=True)
    parent_ids: list[str] = field(factory=list, kw_only=True)
    child_ids: list[str] = field(factory=list, kw_only=True)

    output: Optional[StructureArtifact] = field(default=None, init=False)
    structure: Optional[Structure] = field(default=None, init=False)

    @property
    def parents(self) -> list[Step]:
        return [self.structure.find_step(parent_id) for parent_id in self.parent_ids]

    @property
    def children(self) -> list[Step]:
        return [self.structure.find_step(child_id) for child_id in self.child_ids]

    def add_child(self, child: Step) -> Step:
        if self.structure:
            child.structure = self.structure
        elif child.structure:
            self.structure = child.structure

        if child not in self.structure.steps:
            self.structure.steps.append(child)

        if self not in self.structure.steps:
            self.structure.steps.append(self)

        if child.id not in self.child_ids:
            self.child_ids.append(child.id)

        if self.id not in child.parent_ids:
            child.parent_ids.append(self.id)

        return child

    def add_parent(self, parent: Step) -> Step:
        if self.structure:
            parent.structure = self.structure
        elif parent.structure:
            self.structure = parent.structure

        if parent not in self.structure.steps:
            self.structure.steps.append(parent)

        if self not in self.structure.steps:
            self.structure.steps.append(self)

        if parent.id not in self.parent_ids:
            self.parent_ids.append(parent.id)

        if self.id not in parent.child_ids:
            parent.child_ids.append(self.id)

        return parent

    def is_pending(self) -> bool:
        return self.state == Step.State.PENDING

    def is_finished(self) -> bool:
        return self.state == Step.State.FINISHED

    def is_executing(self) -> bool:
        return self.state == Step.State.EXECUTING

    def before_run(self) -> None:
        pass

    def after_run(self) -> None:
        pass

    def execute(self) -> StructureArtifact:
        try:
            self.state = Step.State.EXECUTING

            self.before_run()

            self.output = self.run()

            self.after_run()
        except Exception as e:
            self.structure.logger.error(f"Step {self.id}\n{e}", exc_info=True)

            self.output = ErrorOutput(str(e), exception=e, step=self)
        finally:
            self.state = Step.State.FINISHED

            return self.output

    def can_execute(self) -> bool:
        return self.state == Step.State.PENDING and all(parent.is_finished() for parent in self.parents)

    def reset(self) -> Step:
        self.state = Step.State.PENDING
        self.output = None

        return self

    @abstractmethod
    def run(self) -> TextOutput:
        ...
