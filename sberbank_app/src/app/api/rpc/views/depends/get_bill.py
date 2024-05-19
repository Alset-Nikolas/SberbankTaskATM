from typing import Optional

from fastapi import Body, Depends
from sqlalchemy import select
from sqlalchemy.engine import Result as ResultSqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.rpc.schemas.responses.errors import BillNotExistError, CurrencyNotExistError
from src.app.api.rpc.views.depends.get_currency import get_currency
from src.app.db.orm import Bill, Currency
from src.app.extensions.sqlalchemy import PoolConnector


async def get_bill_by_denomination_and_currency(
    session: AsyncSession = Depends(PoolConnector.get_session),
    denomination: int = Body(example=500, description='Номинал'),
    currency: Currency = Depends(get_currency),
) -> Optional[Bill]:
    query = select(Bill).where(
        Bill.currency == currency,
        Bill.value == denomination,
    )
    result: ResultSqlalchemy = await session.execute(query)
    bill: Optional[Bill] = result.scalar_one_or_none()
    if not bill:
        raise BillNotExistError()
    return bill
