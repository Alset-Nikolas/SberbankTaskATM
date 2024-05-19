from pydantic import BaseModel


class TransactionBillCreateSchema(BaseModel):
    quantity: int
    transaction_id: int
    bill_id: int
