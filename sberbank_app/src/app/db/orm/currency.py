from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String

from src.app.extensions.sqlalchemy import Base
from src.app.utils.sqlalchemy.association_column import association_relationship
from src.app.utils.sqlalchemy.base_model_mixin import BaseModelMixin

if TYPE_CHECKING:
    from src.app.db.orm import Bill, Transaction


class Currency(Base, BaseModelMixin):
    __tablename__ = 'currencies'
    __mapper_args__ = {'eager_defaults': True}

    id: int = Column(Integer, primary_key=True)

    name: str = Column(String, nullable=False, unique=True)

    bills: list['Bill'] = association_relationship(
        'Bill',
        back_populates='currency',
    )
    transactions: list['Transaction'] = association_relationship(
        'Transaction',
        back_populates='currency',
    )

    def __repr__(self):
        return '<Currency {name}: {msg}>'.format(
            name=self.name,
        )
