from marshmallow import fields, post_load
from griptape.flow.schemas import BaseSchema


class RuleSchema(BaseSchema):
    value = fields.Str()

    @post_load
    def make_obj(self, data, **kwargs):
        from griptape.flow.rules import Rule

        return Rule(**data)
