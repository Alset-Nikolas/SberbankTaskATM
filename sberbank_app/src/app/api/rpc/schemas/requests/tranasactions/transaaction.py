from pydantic import BaseModel

from src.app.enums.transaction_type import TransactionType


class TransactionBillItemCreateSchema(BaseModel):
    quantity: int
    bill_id: int


class TransactionCreateSchema(BaseModel):
    currency_id: int
    type: TransactionType
