import fastapi_jsonrpc as jsonrpc

from src.app.api.rpc.enums.responses.error_status_code.refill import RefillErrorResponseStatusCode


class CurrencyNotExistError(jsonrpc.BaseError):
    CODE = RefillErrorResponseStatusCode.currency_not_exist
    MESSAGE = 'Currency not exist'
