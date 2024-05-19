import fastapi_jsonrpc as jsonrpc
import sentry_sdk
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.urls import init_routers
from src.app.config import settings
from src.app.extensions.logging import logger
from src.app.extensions.sqlalchemy import PoolConnector, init_pool


def create_app() -> FastAPI:
    """
    Create app factory.

    :return: app
    """
    if settings.SENTRY_DSN:
        logger.info('Init sentry')
        sentry_sdk.init(dsn=settings.SENTRY_DSN)

    app = jsonrpc.API(
        title='Sber ATM',
        debug=settings.DEBUG,
        openapi_url=settings.API_PATH_PREF + '/openapi.json',
        docs_url=settings.API_PATH_PREF + '/docs',
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    init_routers(app)
    PoolConnector()
    return app
