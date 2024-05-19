from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, UniqueConstraint

from src.app.extensions.sqlalchemy import Base
from src.app.utils.sqlalchemy import BaseModelMixin
from src.app.utils.sqlalchemy.association_column import AssociationColumn, association_relationship

if TYPE_CHECKING:
    pass


class Bill(Base, BaseModelMixin):
    __tablename__ = 'bills'
    __mapper_args__ = {'eager_defaults': True}
    __table_args__ = (UniqueConstraint('currency_id', 'value'),)

    id: int = Column(Integer, primary_key=True)

    currency_id: int = AssociationColumn(
        'currencies.id',
    )
    currency: 'Currency' = association_relationship(
        'Currency',
        foreign_keys=currency_id,
        back_populates='bills',
    )
    value: int = Column(Integer)

    bank_bills: list['BankBill'] = association_relationship(
        'BankBill',
        back_populates='bill',
    )
    transaction_bill: list['TransactionBill'] = association_relationship(
        'TransactionBill',
        back_populates='bill',
    )

    def __repr__(self):
        return '<Bill currency_id: {currency_id}: {value}>'.format(
            currency_id=self.currency_id,
            value=self.value,
        )
