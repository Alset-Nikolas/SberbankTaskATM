import uuid
from typing import Optional

from pydantic import BaseModel, validator


class IdSchemaMixin(BaseModel):
    id: int

    @validator('id')
    def validate_uuids(cls, value):
        if value:
            return str(value)
        return value


class IdUpdateSchemaMixin(BaseModel):
    id: Optional[int] = None

    @validator('id')
    def validate_uuids(cls, value):
        if value:
            return str(value)
        return value
