from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DECIMAL, Column, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from src.app.enums.transaction_type import TransactionType
from src.app.extensions.sqlalchemy import Base
from src.app.utils.sqlalchemy import BaseModelMixin
from src.app.utils.sqlalchemy.association_column import AssociationColumn, association_relationship
from src.app.utils.sqlalchemy.base_model_mixin import BaseTimeColumnModelMixin
from src.app.utils.sqlalchemy.fields.enum import EnumColumn

if TYPE_CHECKING:
    from src.app.db.orm import Currency, TransactionBill


class Transaction(Base, BaseModelMixin, BaseTimeColumnModelMixin):
    __tablename__ = 'transactions'
    __mapper_args__ = {'eager_defaults': True}

    id: int = Column(Integer, primary_key=True)
    currency_id: int = AssociationColumn(
        'currencies.id',
    )
    currency: 'Currency' = association_relationship(
        'Currency',
        foreign_keys=currency_id,
        back_populates='transactions',
    )
    transaction_bills: list['TransactionBill'] = association_relationship(
        'TransactionBill',
        back_populates='transaction',
    )

    type: str = Column(EnumColumn(TransactionType), nullable=False, default=TransactionType.refill)

    def __repr__(self):
        return '<Transaction ID={id} {type}>'.format(
            id=self.id,
            type=self.type,
        )

    class Enum:
        transaction_type = TransactionType
