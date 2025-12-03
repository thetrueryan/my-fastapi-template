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


class HysteriaConfig(BaseModel):
    container_name: str = "hysteria"
    public_host: str = "127.0.0.1"
    public_port: int = 8443
    acme_email: str = "admin@example.com"
    acme_domain: str = "example.com"
    listen_port: str = ":443"
    masquerade_url: str = "https://bing.com"
    config_path: Path = BASE_PATH / "hysteria" / "config.yaml"


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
    hysteria: HysteriaConfig = HysteriaConfig()


settings = Settings()
