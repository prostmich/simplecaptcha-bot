import configparser
import datetime
from typing import Any, Mapping, Tuple, Union

from pydantic import BaseModel, BaseSettings, validator

from app.misc.paths import BASE_DIR


def ini_file_settings(_: Any) -> Mapping[str, Any]:
    config = configparser.ConfigParser()
    config.read(BASE_DIR / "config.ini")
    return {
        section: values for section, values in config.items() if section != "DEFAULT"
    }


class BotSettings(BaseModel):
    token: str


class WebhookSettings(BaseModel):
    host: str
    path: str

    @validator("host")
    def host_to_url(cls, v: str) -> str:
        if v.startswith("https"):
            return v
        return f"https://{v}"

    @property
    def url(self) -> str:
        if self.host and self.path:
            return f"{self.host}{self.path}"
        return ""


class WebAppSettings(BaseModel):
    host: str
    port: int


class RedisSettings(BaseModel):
    host: str
    port: int = 6379
    db: int
    password: str = ""

    @property
    def connection_uri(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"


class CaptchaSettings(BaseModel):
    duration: Union[int, datetime.timedelta]

    @validator("duration")
    def to_timedelta(cls, v: Union[int, datetime.timedelta]) -> datetime.timedelta:
        if isinstance(v, datetime.timedelta):
            return v
        return datetime.timedelta(seconds=v)


class Settings(BaseSettings):
    bot: BotSettings
    webhook: WebhookSettings
    webapp: WebAppSettings
    redis: RedisSettings
    captcha: CaptchaSettings

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings: Mapping[str, Any],
            env_settings: Mapping[str, Any],
            file_secret_settings: Mapping[str, Any],
        ) -> Tuple:  # type: ignore
            return (
                init_settings,
                ini_file_settings,
                env_settings,
                file_secret_settings,
            )
