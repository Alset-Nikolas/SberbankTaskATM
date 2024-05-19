from typing import Dict, Type

from src.app.utils.sqlalchemy.base_model_mixin import Model, TypeBase


class BaseUpdaterMixin:
    new_data: Dict
    instance: Model

    class Meta:
        model = Type[TypeBase]
