from src.app.db.orm import Transaction
from src.app.utils.pydantic import OrmSchemaMixin


class TransactionSchema(OrmSchemaMixin):
    currency_id: int
    type: Transaction.Enum.transaction_type
