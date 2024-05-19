import fastapi_jsonrpc as jsonrpc

from src.app.api.rpc.enums.responses.error_status_code.refill import RefillErrorResponseStatusCode


class TransactionValueNegativeError(jsonrpc.BaseError):
    CODE = RefillErrorResponseStatusCode.bill_quantity_negative
    MESSAGE = 'Not valid value'
