from pydantic import BaseModel


class BankBillUpdateSchema(BaseModel):
    quantity: int
