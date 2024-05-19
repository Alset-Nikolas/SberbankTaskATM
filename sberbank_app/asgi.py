"""Factory call module."""
import logging

import uvicorn

from src.app.config import settings
from src.app.factory import create_app

app = create_app()

if __name__ == '__main__':
    if settings.DEBUG:
        logging.info(
            'http://{app_host}:{app_port}{path_doc}'.format(
                app_host=settings.APP_HOST,
                app_port=settings.APP_PORT,
                path_doc=app.docs_url,
            ),
        )
    uvicorn.run(
        app='asgi:app',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.DEBUG,
        reload=settings.RELOAD,
    )
