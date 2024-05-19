import logging
import os
from typing import Optional, Union

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Base settings."""

    # app
    DEBUG: bool
    RELOAD: bool
    NAME: str = 'sberbank-task-atm'
    LOG_LEVEL: int = logging.WARNING
    USE_JSON_LOG_FORMAT: bool = False
    API_PATH_PREF: str = '/api/v1'
    APP_HOST: str
    APP_PORT: int = 8090

    CORS_ORIGINS: list = [
        '*',
    ]

    # sentry
    SENTRY_DSN: str = ''

    # postgres
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'qwerty'
    POSTGRES_DB: str = 'sberbank_task_atm'
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_ECHO: bool = False

    class Config:
        env_file_encoding = 'utf-8'


class LocalSettings(Settings):
    DEBUG: bool = True
    RELOAD: bool = True
    APP_HOST: str = 'localhost'

    POSTGRES_HOST: str = '127.0.0.1'
    POSTGRES_PORT: int = 5432

    SENTRY_DSN: Optional[str] = None


class DockerSettings(Settings):
    DEBUG: bool = False
    RELOAD: bool = False
    APP_HOST: str = '0.0.0.0'

    POSTGRES_HOST: str = 'sberbank_app_postgres'
    POSTGRES_PORT: int = 5432


def get_settings() -> Union[DockerSettings, LocalSettings]:
    env_type = os.environ['TYPE_ENV']
    config_cls_dict = {
        'docker': DockerSettings,
        'local': LocalSettings,
    }
    config_cls = config_cls_dict[env_type]
    return config_cls()


settings = get_settings()
