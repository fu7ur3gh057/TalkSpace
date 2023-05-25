import enum
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "0.0.0.0"
    # host: str = "127.0.0.1"
    port: int = 8066
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = True

    # JWT Security variables
    access_token_expire_minutes = 30  # 30 minutes
    refresh_token_expire_minutes = 60 * 24 * 7  # 7 days
    algorithm = "HS256"
    # JWT secrets
    jwt_secret_key = "access_1238u12831dhasdhjasdjasjdh"
    jwt_refresh_secret_key = "refresh_3214kjkafskdjakfjklsfk"

    # Current environment
    environment: str = "dev"
    # Path of local temp directory
    temp_dir: str = "/temp"
    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_host: str = "localhost"
    # db_host: str = "postgres"
    db_port: int = 5432
    db_user: str = "postgres"
    db_pass: str = "1234"
    db_base: str = "helper_chat_db"
    db_echo: bool = False

    # Variables for Redis
    redis_host: str = "localhost"
    # redis_host: str = "redis"
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[int] = None
    celery_url: str = "redis://redis:6379"

    # celery_url: str = "redis://localhost:6379"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )

    class Config:
        env_file = ".env"
        env_prefix = "HELPER"
        env_file_encoding = "utf-8"


settings = Settings()
