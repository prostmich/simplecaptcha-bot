import logging
from typing import Any, Dict, cast

from aiogram import Bot
from arq import run_worker
from arq.connections import RedisSettings
from arq.typing import WorkerSettingsType

from app.misc.settings_reader import Settings
from app.services.lock_user import LockUserService
from worker.tasks.join_expired import join_expired_task

settings = Settings()


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )


async def startup(ctx: Dict[str, Any]):
    ctx["bot"] = Bot(token=settings.bot.token, parse_mode="html")
    ctx["lock_user_service"] = LockUserService(
        connection_uri=settings.redis.connection_uri,
    )


async def shutdown(ctx: Dict[str, Any]):
    bot: Bot = ctx.pop("bot")
    await bot.session.close()


class WorkerSettings:
    on_startup = startup
    on_shutdown = shutdown
    functions = [join_expired_task]
    allow_abort_jobs = True


if __name__ == "__main__":
    configure_logging()
    redis_settings = RedisSettings.from_dsn(settings.redis.connection_uri)
    settings_cls = cast(WorkerSettingsType, WorkerSettings)
    run_worker(settings_cls, redis_settings=redis_settings)
