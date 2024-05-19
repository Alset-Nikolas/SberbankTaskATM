from typing import Type, TypeVar

from src.app.extensions.sqlalchemy import Base

TypeBaseModel = TypeVar('TypeBaseModel', bound=Base)


class ErrorUpdateObject(Exception):
    def __init__(self, model: Type[TypeBaseModel], description: str, field_name: str = '') -> None:
        self.model = model
        self.message = description
        self.field_name = field_name
        self.description = description
        super().__init__(self.message)
