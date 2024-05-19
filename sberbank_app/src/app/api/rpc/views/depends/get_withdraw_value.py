from typing import Optional

from fastapi import Body, Depends
from sqlalchemy import select
from sqlalchemy.engine import Result as ResultSqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.rpc.schemas.responses.errors import BillQuantityNegativeError, CurrencyNotExistError
from src.app.api.rpc.schemas.responses.errors.validations.transaction_value_negative import (
    TransactionValueNegativeError,
)
from src.app.db.orm import Bill, Currency
from src.app.extensions.sqlalchemy import PoolConnector


async def get_withdraw_value(
    value: int = Body(examples=1000, description='Сумма', default=1000),
) -> Currency:

    if value <= 0:
        raise TransactionValueNegativeError()
    return value
