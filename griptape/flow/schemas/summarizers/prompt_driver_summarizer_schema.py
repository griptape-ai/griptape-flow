from marshmallow import fields
from griptape.flow.schemas import PolymorphicSchema, SummarizerSchema


class PromptDriverSummarizerSchema(SummarizerSchema):
    driver = fields.Nested(PolymorphicSchema())

    def make_obj(self, data, **kwargs):
        from griptape.flow.summarizers import PromptDriverSummarizer

        return PromptDriverSummarizer(**data)
