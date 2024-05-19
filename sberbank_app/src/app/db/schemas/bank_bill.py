from src.app.utils.pydantic import BaseOrmSchemaMixin


class BankBillSchema(BaseOrmSchemaMixin):
    bill_id: int
    quantity: int
