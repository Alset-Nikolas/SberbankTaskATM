from decimal import Decimal
from enum import Enum
from typing import Tuple

from src.app.config import settings
from src.app.utils.sqlalchemy.fields.enum import MixinEnum


class TransactionType(str, MixinEnum):
    refill = 'refill'
    withdraw = 'withdraw'
