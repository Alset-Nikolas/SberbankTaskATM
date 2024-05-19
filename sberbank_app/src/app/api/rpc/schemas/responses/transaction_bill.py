from src.app.db.schemas import BillSchema, TransactionBillSchema


class TransactionBillResponseSchema(TransactionBillSchema):
    bill_id: BillSchema
