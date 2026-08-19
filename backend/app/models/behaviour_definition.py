from pydantic import BaseModel, Enum


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class BehaviourDefinition(BaseModel):
    action: str
    field: str