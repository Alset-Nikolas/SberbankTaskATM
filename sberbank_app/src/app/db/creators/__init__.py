from src.app.db.creators.exceptions import ErrorCreateObject, ErrorUniqObjectExist
from src.app.db.creators.faker import fake
from src.app.db.creators.meta_base import FactoryUseMode

FP: str = 'src.app.db.creators.'
# Перечисляем абсолютные пути до фабрик для избежания циклического импорта
currency_creator: str = FP + 'CurrencyCreator'
bill_creator: str = FP + 'BillCreator'
bank_bill_creator: str = FP + 'BankBillCreator'
transaction_creator: str = FP + 'TransactionCreator'

transaction_bills_creator: str = FP + 'TransactionBillsCreator'

from src.app.db.creators.models import TransactionBillCreator, TransactionCreator
