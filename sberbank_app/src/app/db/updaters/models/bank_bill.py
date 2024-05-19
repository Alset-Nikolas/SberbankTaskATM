from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.orm import BankBill
from src.app.db.schemas import BankBillSchema
from src.app.db.updaters.exceptions import ErrorUpdateObject


class BankBillUpdater:
    def __init__(
        self,
        session: AsyncSession,
        instance: Union[BankBill, int],
        new_data: dict,
        commit: bool = True,
    ):
        """
        Обновление. Здесь сосредоточены бизнес правила
        :param session:
        :param instance: скилл, который меняют
        :param new_data: новые данные
        :param commit: коммитеть изменения или нет
        """
        self.session = session

        self.instance_id: int = instance.id if isinstance(instance, BankBill) else instance
        self.new_data = new_data
        self.commit = commit
        self.old_data: Optional[BankBillSchema] = None
        self.instance: Optional[BankBill] = None
        self.is_update: bool = False

    async def update(self) -> BankBill:
        self.instance = await BankBill.get_by_id(self.instance_id, session=self.session)
        self.old_data: BankBillSchema = BankBillSchema.from_orm(self.instance)
        self._update_quantity()

        if self.is_update:
            await self.instance.save(session=self.session, commit=self.commit)
        return self.instance

    def _update_quantity(self) -> None:
        name_field: str = 'quantity'
        value = self.new_data.get(name_field)
        if value is None or value == getattr(self.instance, name_field):
            return
        if value < 0:
            raise ErrorUpdateObject(
                model=BankBill,
                description='quantity not negative',
                field_name='quantity',
            )
        self.is_update = True
        self.instance.quantity = value
