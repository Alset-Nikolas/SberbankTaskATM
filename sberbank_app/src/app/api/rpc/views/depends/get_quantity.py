from typing import Optional

from fastapi import Body, Depends
from sqlalchemy import select
from sqlalchemy.engine import Result as ResultSqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.rpc.schemas.responses.errors import BillQuantityNegativeError, CurrencyNotExistError
from src.app.db.orm import Bill, Currency
from src.app.extensions.sqlalchemy import PoolConnector


async def get_quantity_positive(
    quantity: int = Body(examples=5, description='Кол-во купюр', default=1),
) -> Currency:

    if quantity <= 0:
        raise BillQuantityNegativeError()
    return quantity
