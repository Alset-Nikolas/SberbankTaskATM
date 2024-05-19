from typing import Dict, List

from fastapi import Depends
from sqlalchemy import desc, select
from sqlalchemy.engine import Result as ResultSqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.api.rpc.schemas.requests.bank_bill import BankBillUpdateSchema
from src.app.api.rpc.schemas.requests.tranasactions.transaaction import (
    TransactionBillItemCreateSchema,
    TransactionCreateSchema,
)
from src.app.api.rpc.schemas.responses.errors import NotEnoughBankFundsError
from src.app.api.rpc.schemas.responses.withdraw import TransactionBillItemResponseSchema, WithdrawResponseSchema
from src.app.api.rpc.views.depends.get_currency import get_currency
from src.app.api.rpc.views.depends.get_withdraw_value import get_withdraw_value
from src.app.db.creators.models.transactions.transaction import TransactionCreator
from src.app.db.orm import BankBill, Bill, Currency, Transaction
from src.app.db.schemas import TransactionSchema
from src.app.db.updaters.models.bank_bill import BankBillUpdater
from src.app.enums.transaction_type import TransactionType
from src.app.extensions.sqlalchemy import PoolConnector


async def get_bank_bills_by_currency(
    session: AsyncSession = Depends(PoolConnector.get_session),
    currency: Currency = Depends(get_currency),
    value: int = Depends(get_withdraw_value),
) -> List[BankBill]:
    query = (
        select(
            BankBill,
        )
        .join(
            Bill,
            BankBill.bill_id == Bill.id,
        )
        .options(joinedload(BankBill.bill))
        .where(
            Bill.currency == currency,
            BankBill.quantity > 0,
            Bill.value <= value,
        )
        .order_by(
            desc(Bill.value),
        )
    )

    result: ResultSqlalchemy = await session.execute(query)
    return result.scalars()


async def get_transaction_bill_items(bank_bills: List[BankBill], value: int):
    value_copy = value
    result = {}
    for bank_bill in bank_bills:
        if bank_bill.bill.value > value_copy:
            continue
        if bank_bill.bill not in result:
            result[bank_bill.bill] = 0
        delta_bill_quantity = min(bank_bill.quantity, value_copy // bank_bill.bill.value)
        result[bank_bill.bill] = delta_bill_quantity
        value_copy -= delta_bill_quantity * bank_bill.bill.value
    if value_copy > 0:
        raise NotEnoughBankFundsError()
    return result


async def withdraw(
    session: AsyncSession = Depends(PoolConnector.get_session),
    value: int = Depends(get_withdraw_value),
    currency: Currency = Depends(get_currency),
    bank_bills: List[BankBill] = Depends(get_bank_bills_by_currency),
) -> WithdrawResponseSchema:
    '''
    Получить деньги.
    _______________
    Банкомат для заданной суммы выдает массив с номиналом и количеством купюр, в зависимости от доступных купюр в банкомате.
    _______________
    Если денег недостаточно, банкомат выдает сообщение/ошибку, что недостаточно денег.
    ______________
    Например: 1000 рублей
    '''
    bill_quantity: Dict[Bill, int] = await get_transaction_bill_items(bank_bills, value)
    transaction: Transaction = await TransactionCreator(
        **TransactionCreateSchema(
            currency_id=currency.id,
            type=TransactionType.withdraw,
        ).dict(),
        session=session,
        transaction_bills=[
            TransactionBillItemCreateSchema(
                quantity=quantity,
                bill_id=bill.id,
            )
            for bill, quantity in bill_quantity.items()
        ],
        commit_model=False,
    ).create()
    for bill, quantity in bill_quantity.items():
        bank_bill = await BankBill.get_or_none(session=session, id_=bill.id)

        await BankBillUpdater(
            session=session,
            instance=bank_bill,
            new_data=BankBillUpdateSchema(
                quantity=bank_bill.quantity - quantity,
            ).dict(),
            commit=False,
        ).update()

    await session.commit()
    return WithdrawResponseSchema(
        transaction=TransactionSchema.from_orm(transaction),
        transaction_bills=[
            TransactionBillItemResponseSchema(
                quantity=quantity,
                bill=bill,
                currency=currency,
            )
            for bill, quantity in bill_quantity.items()
        ],
    )
