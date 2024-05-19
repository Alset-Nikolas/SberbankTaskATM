import fastapi_jsonrpc as jsonrpc

from src.app.api.rpc.enums.responses.error_status_code.refill import RefillErrorResponseStatusCode


class NotEnoughBankFundsError(jsonrpc.BaseError):
    CODE = RefillErrorResponseStatusCode.bill_not_exist
    MESSAGE = 'Not enough bank funds'
