from pydantic import BaseModel, Field

from app.models.behaviour_definition import BehaviourDefinition, HttpMethod
from app.models.schema_definition import SchemaDefinition


class RouteDefinition(BaseModel):
    path: str
    methods: list[HttpMethod]
    route_schema: SchemaDefinition = Field(..., alias="schema")
    behaviours: dict[HttpMethod, BehaviourDefinition]

    model_config = {"populate_by_name": True}
