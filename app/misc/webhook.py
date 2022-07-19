from aiogram import Bot, Dispatcher
from aiogram.dispatcher.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from aiohttp import web

from app.misc.settings_reader import Settings


def configure_app(dp: Dispatcher, bot: Bot, settings: Settings) -> web.Application:
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot, settings=settings).register(
        app, path=settings.webhook.path
    )
    setup_application(app, dp, bot=bot)
    return app
