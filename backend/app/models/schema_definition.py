from pydantic import BaseModel, Literal


class FieldDefinition(BaseModel):
    type: Literal["str", "int", "bool"]


class SchemaDefinition(BaseModel):
    type: Literal["object"]
    properties: dict[str, FieldDefinition]
