from src.app.utils.pydantic.orm_schema import BaseOrmSchemaMixin


class BillSchema(BaseOrmSchemaMixin):
    currency_id: int
    value: int
