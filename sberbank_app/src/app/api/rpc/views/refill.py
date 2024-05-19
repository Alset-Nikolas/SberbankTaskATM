from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.rpc.schemas.requests.bank_bill import BankBillUpdateSchema
from src.app.api.rpc.schemas.requests.tranasactions.transaaction import (
    TransactionBillItemCreateSchema,
    TransactionCreateSchema,
)
from src.app.api.rpc.views.depends.get_bank_bill import get_bank_bill
from src.app.api.rpc.views.depends.get_bill import get_bill_by_denomination_and_currency
from src.app.api.rpc.views.depends.get_currency import get_currency
from src.app.api.rpc.views.depends.get_quantity import get_quantity_positive
from src.app.db.creators.models.transactions.transaction import TransactionCreator
from src.app.db.orm import BankBill, Bill, Currency, Transaction
from src.app.db.schemas import TransactionSchema
from src.app.db.updaters.models.bank_bill import BankBillUpdater
from src.app.enums.transaction_type import TransactionType
from src.app.extensions.sqlalchemy import PoolConnector


async def refill(
    session: AsyncSession = Depends(PoolConnector.get_session),
    bill: Bill = Depends(get_bill_by_denomination_and_currency),
    bank_bill: BankBill = Depends(get_bank_bill),
    currency: Currency = Depends(get_currency),
    quantity: int = Depends(get_quantity_positive),
) -> TransactionSchema:
    '''
    Положить деньги.
    _____________
    За один раз можно положить несколько купюра одного наминала.
    ___________
    Например: 1 купюру по 500 рублей
    '''
    transaction: Transaction = await TransactionCreator(
        **TransactionCreateSchema(
            currency_id=currency.id,
            type=TransactionType.refill,
        ).dict(),
        session=session,
        transaction_bills=[
            TransactionBillItemCreateSchema(
                quantity=quantity,
                bill_id=bill.id,
            ),
        ],
        commit_model=False,
    ).create()
    await BankBillUpdater(
        session=session,
        instance=bank_bill,
        new_data=BankBillUpdateSchema(
            quantity=bank_bill.quantity + quantity,
        ).dict(),
        commit=False,
    ).update()
    await session.commit()
    return TransactionSchema.from_orm(transaction)
