from pydantic import BaseModel

from app.models.route_definition import RouteDefinition


class ApiDefinition(BaseModel):
    api_id: str
    name: str
    routes: list[RouteDefinition]
