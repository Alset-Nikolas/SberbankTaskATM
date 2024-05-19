import fastapi_jsonrpc as jsonrpc

from src.app.api.rpc.schemas.responses.errors import (
    BillNotExistError,
    BillQuantityNegativeError,
    CurrencyNotExistError,
    NotEnoughBankFundsError,
)
from src.app.api.rpc.schemas.responses.errors.validations.transaction_value_negative import (
    TransactionValueNegativeError,
)
from src.app.api.rpc.views.refill import refill
from src.app.api.rpc.views.withdraw import withdraw


def add_rpc_routers(app: jsonrpc.API) -> None:
    api_v1: jsonrpc.Entrypoint = jsonrpc.Entrypoint(
        path='/api/gpt-back/jsonrpc',
        tags=['JSON-RPC'],
    )

    api_v1.add_method_route(
        func=refill,
        errors=[
            CurrencyNotExistError,
            BillQuantityNegativeError,
            BillNotExistError,
        ],
    )
    api_v1.add_method_route(
        func=withdraw,
        errors=[
            CurrencyNotExistError,
            NotEnoughBankFundsError,
            TransactionValueNegativeError,
        ],
    )

    app.bind_entrypoint(ep=api_v1)
