from src.app.utils.pydantic import IdSchemaMixin
from src.app.utils.pydantic.timestamp_schema import TimestampSchemaMixin


class BaseOrmSchemaMixin(IdSchemaMixin):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class OrmSchemaMixin(IdSchemaMixin, TimestampSchemaMixin):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
