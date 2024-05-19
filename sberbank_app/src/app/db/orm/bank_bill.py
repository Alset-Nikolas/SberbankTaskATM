from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer

from src.app.extensions.sqlalchemy import Base
from src.app.utils.sqlalchemy import BaseModelMixin
from src.app.utils.sqlalchemy.association_column import AssociationColumn, association_relationship

if TYPE_CHECKING:
    pass


class BankBill(Base, BaseModelMixin):
    __tablename__ = 'bank_bills'
    __mapper_args__ = {'eager_defaults': True}

    id: int = Column(Integer, primary_key=True)

    bill_id: int = AssociationColumn(
        'bills.id',
    )
    bill: 'Bill' = association_relationship(
        'Bill',
        foreign_keys=bill_id,
        back_populates='bank_bills',
    )
    quantity: int = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return '<BankBill bill={bill}, quantity={quantity}>'.format(
            bill=self.bill if self.bill else self.bill_id,
            quantity=self.quantity,
        )
