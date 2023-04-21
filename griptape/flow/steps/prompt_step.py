from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from attr import define, field
from griptape.flow.utils import J2
from griptape.flow.steps import Step
from griptape.flow.artifacts import TextOutput

if TYPE_CHECKING:
    from griptape.flow.drivers import BasePromptDriver


@define
class PromptStep(Step):
    prompt_template: str = field(default="{{ args[0] }}")
    context: dict[str, any] = field(factory=dict, kw_only=True)
    driver: Optional[BasePromptDriver] = field(default=None, kw_only=True)

    def before_run(self) -> None:
        super().before_run()

        self.structure.logger.info(f"Step {self.id}\nInput: {self.render_prompt()}")

    def run(self) -> TextOutput:
        self.output = self.active_driver().run(value=self.structure.to_prompt_string(self))

        return self.output

    def after_run(self) -> None:
        super().after_run()

        self.structure.logger.info(f"Step {self.id}\nOutput: {self.output.value}")

    def active_driver(self) -> BasePromptDriver:
        if self.driver is None:
            return self.structure.prompt_driver
        else:
            return self.driver

    def render_prompt(self) -> str:
        return J2().render_from_string(
            self.prompt_template,
            **self.full_context
        )

    def render(self) -> str:
        return J2("prompts/steps/prompt.j2").render(
            step=self
        )

    @property
    def full_context(self) -> dict[str, any]:
        structure_context = self.structure.context(self)

        structure_context.update(self.context)

        return structure_context
