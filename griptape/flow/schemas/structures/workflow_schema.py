from marshmallow import post_load
from griptape.flow.schemas import StructureSchema


class WorkflowSchema(StructureSchema):
    @post_load
    def make_obj(self, data, **kwargs):
        from griptape.flow.structures import Workflow

        return Workflow(**data)
