from typing import Any, Dict, Optional

from src.app.db.creators import ErrorCreateObject, bill_creator, transaction_creator
from src.app.db.creators.meta_base import BaseFactory, create_model
from src.app.db.orm import Bill, Transaction, TransactionBill
from src.app.utils.async_partial import async_partial


class TransactionBillCreator(BaseFactory[TransactionBill]):
    """Фабрика TransactionBill."""

    class Meta:
        model = TransactionBill

    data_fake = {
        'quantity': 5,
        'transaction_id': async_partial(create_model, factory=transaction_creator),
        'bill_id': async_partial(create_model, factory=bill_creator),
    }

    async def create(self) -> Transaction:
        return await self._create()

    async def before_create(
        self,
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Подготавливаем данные и проверяем удовлетворяемость инвариантам.
        Порядок задания данных ВАЖЕН!!!
        :param kwargs:
        :return:
        """

        data_for_create: Dict[str, Any] = {}
        self.default_setter('quantity', input_data=kwargs, new_instance_as_dict=data_for_create)
        await self._set_transaction_id(kwargs, data_for_create)
        await self._set_bill_id(kwargs, data_for_create)
        return data_for_create

    async def _set_transaction_id(self, kwargs: Dict[str, Any], data_for_create: Dict[str, Any]) -> None:
        name_field: str = 'transaction_id'
        value = kwargs.get(name_field)
        transaction: Optional[Transaction] = await Transaction.get_or_none(session=self.session, id_=value)
        if not transaction:
            raise ErrorCreateObject(
                model=Transaction,
                description='Transaction not exist id={}'.format(value),
                field_name='transaction_id',
            )
        data_for_create[name_field] = value

    async def _set_bill_id(self, kwargs: Dict[str, Any], data_for_create: Dict[str, Any]) -> None:
        name_field: str = 'bill_id'
        value = kwargs.get(name_field)
        bill: Optional[Bill] = await Bill.get_or_none(session=self.session, id_=value)
        if not bill:
            raise ErrorCreateObject(
                model=Bill,
                description='Bill not exist id={}'.format(value),
                field_name='bill_id',
            )
        data_for_create[name_field] = value
