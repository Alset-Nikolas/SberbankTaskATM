from typing import List

from pydantic import BaseModel

from src.app.db.schemas import BillSchema, CurrencySchema, TransactionSchema


class TransactionBillItemResponseSchema(BaseModel):
    quantity: int
    bill: BillSchema
    currency: CurrencySchema


class WithdrawResponseSchema(BaseModel):
    transaction: TransactionSchema
    transaction_bills: List[TransactionBillItemResponseSchema]
