import fastapi_jsonrpc as jsonrpc

from src.app.api.rpc.enums.responses.error_status_code.refill import RefillErrorResponseStatusCode


class BillNotExistError(jsonrpc.BaseError):
    CODE = RefillErrorResponseStatusCode.bill_not_exist
    MESSAGE = 'Bill not exist'
