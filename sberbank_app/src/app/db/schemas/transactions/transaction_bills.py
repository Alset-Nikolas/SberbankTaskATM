from src.app.utils.pydantic import OrmSchemaMixin


class TransactionBillSchema(OrmSchemaMixin):
    quantity: int
    transaction_id: int
    bill_id: int
