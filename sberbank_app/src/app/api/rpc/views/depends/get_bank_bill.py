from select import select
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.engine import Result as ResultSqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.rpc.schemas.responses.errors import CurrencyNotExistError
from src.app.api.rpc.views.depends.get_bill import get_bill_by_denomination_and_currency
from src.app.db.orm import BankBill, Bill, Currency
from src.app.extensions.sqlalchemy import PoolConnector


async def get_bank_bill(
    session: AsyncSession = Depends(PoolConnector.get_session),
    bill: Bill = Depends(get_bill_by_denomination_and_currency),
) -> BankBill:
    query = select(BankBill).where(
        BankBill.bill == bill,
    )
    result: ResultSqlalchemy = await session.execute(query)
    return result.scalar()
