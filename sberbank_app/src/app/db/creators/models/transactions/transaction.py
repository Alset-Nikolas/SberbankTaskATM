from typing import Any, Dict, List, Optional

from src.app.api.rpc.schemas.requests.tranasactions.transaaction import TransactionBillItemCreateSchema
from src.app.api.rpc.schemas.requests.tranasactions.transaction_bill import TransactionBillCreateSchema
from src.app.db.creators import ErrorCreateObject
from src.app.db.creators.meta_base import BaseFactory, ExceptionBreak
from src.app.db.creators.models.transactions.transaction_bill import TransactionBillCreator
from src.app.db.orm import Bill, Currency, Transaction
from src.app.enums.transaction_type import TransactionType


class TransactionCreator(BaseFactory[Transaction]):
    """Фабрика Transaction."""

    class Meta:
        model = Transaction

    data_fake = {
        # 'currency_id': async_partial(create_model, factory=currency_creator),
        'type': TransactionType.refill,
    }

    def __init__(
        self,
        transaction_bills: List[TransactionBillItemCreateSchema],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.transaction_bills: List[TransactionBillItemCreateSchema] = transaction_bills

    async def create(self) -> Transaction:
        return await self._create()

    async def before_create(
        self,
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        :param kwargs:
        :return:
        """

        data_for_create: Dict[str, Any] = {}
        self.default_setter('type', input_data=kwargs, new_instance_as_dict=data_for_create)
        await self._set_currency_id(kwargs, data_for_create)
        await self._check_transaction_item_bills(kwargs, data_for_create)

        return data_for_create

    async def _check_transaction_item_bills(self, kwargs: Dict[str, Any], data_for_create: Dict[str, Any]) -> None:
        bills_currencies = set()
        bills_bill_ids = set()
        for i, transaction_bill_item_schema in enumerate(self.transaction_bills):
            transaction_bill_item_schema: TransactionBillItemCreateSchema
            bill: Optional[Bill] = await Bill.get_or_none(
                session=self.session,
                id_=transaction_bill_item_schema.bill_id,
            )
            if not bill:
                raise ErrorCreateObject(
                    model=Transaction,
                    description='Bills: Bill not exist id={}'.format(transaction_bill_item_schema.bill_id),
                    field_name='bills[{i}].bill_id'.format(i=i),
                )
            bills_currencies.add(
                bill.currency,
            )
            bills_bill_ids.add(
                bill.id,
            )
        if len(bills_currencies) != 1 or len(self.transaction_bills) == 0:
            raise ErrorCreateObject(
                model=Transaction,
                description='Bills currency in transactions not diff and not empty: {}'.format(bills_currencies),
                field_name='bills',
            )
        if len(bills_bill_ids) != len(self.transaction_bills):
            raise ErrorCreateObject(
                model=Transaction,
                description='Bills ids not repeat',
                field_name='bills',
            )

    async def _set_currency_id(self, kwargs: Dict[str, Any], data_for_create: Dict[str, Any]) -> None:
        name_field: str = 'currency_id'
        value = kwargs.get(name_field)
        currency: Optional[Currency] = await Currency.get_or_none(session=self.session, id_=value)
        if not currency:
            raise ErrorCreateObject(
                model=Transaction,
                description='Currency not exist id={}'.format(value),
                field_name='currency_id',
            )
        data_for_create[name_field] = value

    async def before_commit(self, result_data: Transaction) -> None:
        """
        Выполняет логику после создания объекта, но до commit в БД.

        :param result_data: очищенные данные для создания сущности.
        """
        bills = []
        for i, transaction_bills in enumerate(self.transaction_bills):

            try:
                bills.append(
                    await TransactionBillCreator(
                        **TransactionBillCreateSchema(
                            quantity=transaction_bills.quantity,
                            transaction_id=result_data.id,
                            bill_id=transaction_bills.bill_id,
                        ).dict(),
                        session=self.session,
                        commit_model=False,
                    ).create(),
                )
            except ErrorCreateObject as ex:
                await self.session.rollback()
                raise ExceptionBreak(
                    model=Transaction,
                    description='Bills: Bill create err {}'.format(ex.description),
                    field_name='bills[{i}].bill_id'.format(i=i),
                )
        result_data.transaction_bills = bills
