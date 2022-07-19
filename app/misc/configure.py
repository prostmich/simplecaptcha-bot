import logging
from typing import Any, Dict

from app.misc.settings_reader import Settings
from app.services.captcha import CaptchaService
from app.services.captcha_generator import CaptchaGenerator
from app.services.captcha_scheduler import CaptchaScheduler
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
    return {"captcha": captcha}


def configure_logging() -> None:
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
