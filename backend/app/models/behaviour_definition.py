from enum import StrEnum

from pydantic import BaseModel


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class BehaviourDefinition(BaseModel):
    action: str
    field: str
