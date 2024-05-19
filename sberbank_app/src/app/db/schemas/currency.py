from src.app.utils.pydantic.orm_schema import BaseOrmSchemaMixin


class CurrencySchema(BaseOrmSchemaMixin):
    name: str
