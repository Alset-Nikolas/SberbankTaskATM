from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer

from src.app.enums.transaction_type import TransactionType
from src.app.extensions.sqlalchemy import Base
from src.app.utils.sqlalchemy import BaseModelMixin
from src.app.utils.sqlalchemy.association_column import AssociationColumn, association_relationship
from src.app.utils.sqlalchemy.base_model_mixin import BaseTimeColumnModelMixin
from src.app.utils.sqlalchemy.fields.enum import EnumColumn

if TYPE_CHECKING:
    from src.app.db.orm import Bill, Transaction


class TransactionBill(Base, BaseModelMixin, BaseTimeColumnModelMixin):
    __tablename__ = 'transaction_bills'
    __mapper_args__ = {'eager_defaults': True}

    id: int = Column(Integer, primary_key=True)
    quantity: int = Column(Integer, nullable=False)

    transaction_id: int = AssociationColumn(
        'transactions.id',
    )
    transaction: 'Transaction' = association_relationship(
        'Transaction',
        foreign_keys=transaction_id,
        back_populates='transaction_bills',
    )

    bill_id: int = AssociationColumn(
        'bills.id',
    )
    bill: 'Bill' = association_relationship(
        'Bill',
        foreign_keys=bill_id,
        back_populates='transaction_bill',
    )

    def __repr__(self):
        return '<TransactionBills ID={id} transaction_id={transaction_id}> bill_id={bill_id}'.format(
            id=self.id,
            transaction_id=self.transaction_id,
            bill_id=self.bill_id,
        )
