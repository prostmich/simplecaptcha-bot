import logging
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.misc.paths import RESOURCES_DIR
from app.misc.settings_reader import Settings
from app.services.captcha import CaptchaService
from app.services.captcha_generator import CaptchaGenerator
from app.services.captcha_scheduler import CaptchaScheduler
from app.services.fluent import FluentService, LocalesDataLoader
from app.services.lock_user import LockUserService


async def configure_services(settings: Settings) -> Dict[str, Any]:
    lock_service = LockUserService(connection_uri=settings.redis.connection_uri)
    captcha_scheduler = CaptchaScheduler()
    captcha_generator = CaptchaGenerator()
    captcha = CaptchaService(
        lock_service,
        captcha_scheduler,
        captcha_generator,
        captcha_duration=settings.captcha.duration,
    )
    await captcha_scheduler.init(connection_uri=settings.redis.connection_uri)
    captcha_generator.load_emoji()
    return {
        "captcha": captcha,
        "fluent": _configure_fluent(),
    }


def configure_postgres(settings: Settings) -> sessionmaker:
    engine = create_async_engine(
        settings.postgres.connection_uri,
        future=True,
    )
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def configure_logging() -> None:
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )


def _configure_fluent():
    locales_map = {
        "ru": ("ru", "en"),
        "en": ("en", "ru"),
    }
    locales = LocalesDataLoader(RESOURCES_DIR / "text").get_locales()
    return FluentService(locales_map, locales)
