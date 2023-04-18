from abc import abstractmethod
from marshmallow import fields
from marshmallow_enum import EnumField
from griptape.flow.schemas import BaseSchema
from griptape.flow.steps import Step


class StepSchema(BaseSchema):
    class Meta:
        ordered = True

    id = fields.Str()
    state = EnumField(Step.State)
    parent_ids = fields.List(fields.Str())
    child_ids = fields.List(fields.Str())

    @abstractmethod
    def make_obj(self, data, **kwargs):
        ...
