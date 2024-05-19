import fastapi_jsonrpc as jsonrpc

from src.app.api.rpc.routers import add_rpc_routers


def init_routers(app: jsonrpc.API) -> None:
    add_rpc_routers(app)
