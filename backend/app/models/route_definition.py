from pydantic import BaseModel

from app.models.behaviour_definition import BehaviourDefinition, HttpMethod
from app.models.schema_definition import SchemaDefinition


class RouteDefinition(BaseModel):
    path: str
    methods: list[HttpMethod]
    schema: SchemaDefinition
    behaviours: dict[HttpMethod, BehaviourDefinition]