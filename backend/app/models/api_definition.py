from pydantic import BaseModel

from app.models.route_definition import RouteDefinition


class ApiDefinition(BaseModel):
    id: str
    routes: list[RouteDefinition]
