from typing import Optional

from fastapi import Body, Depends
from sqlalchemy import select
from sqlalchemy.engine import Result as ResultSqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.rpc.schemas.responses.errors import CurrencyNotExistError
from src.app.db.orm import Bill, Currency
from src.app.extensions.sqlalchemy import PoolConnector


async def get_currency(
    session: AsyncSession = Depends(PoolConnector.get_session),
    currency: str = Body(examples='RUB', description='Валюта', default='RUB'),
) -> Currency:
    query = select(Currency).where(
        Currency.name == currency,
    )
    result: ResultSqlalchemy = await session.execute(query)
    currency: Optional[Currency] = result.scalar_one_or_none()
    if not currency:
        raise CurrencyNotExistError()
    return currency
