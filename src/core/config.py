import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_PATH = Path(__file__).resolve().parent.parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class LoggerConfig(BaseModel):
    logger_lvl: int = logging.INFO
    logger_path: Path = BASE_PATH / "logs" / "app_logs.log"


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DbConfig(BaseModel):
    host: str = "localhost"
    passwd: str | None = None
    user: str = "postgres"
    name: str = "postgres"
    port: int = 5432

    convention: dict = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url_async(self):
        return f"postgresql+asyncpg://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_PATH / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    logger_config: LoggerConfig = LoggerConfig()
    api: ApiPrefix = ApiPrefix()
    run: RunConfig = RunConfig()
    db: DbConfig


settings = Settings()