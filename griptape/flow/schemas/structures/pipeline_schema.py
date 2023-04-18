from marshmallow import post_load, fields
from griptape.flow.schemas import StructureSchema


class PipelineSchema(StructureSchema):
    autoprune_memory = fields.Bool()

    @post_load
    def make_obj(self, data, **kwargs):
        from griptape.flow.structures import Pipeline

        return Pipeline(**data)
