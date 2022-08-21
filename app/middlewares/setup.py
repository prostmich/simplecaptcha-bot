from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from app.middlewares.db import DatabaseMiddleware
from app.middlewares.entities import EntitiesMiddleware


def setup_middlewares(dp: Dispatcher, session_maker: sessionmaker):
    dp.update.outer_middleware.register(DatabaseMiddleware(session_maker))

    dp.message.outer_middleware.register(EntitiesMiddleware())
    dp.callback_query.outer_middleware.register(EntitiesMiddleware())
    dp.my_chat_member.outer_middleware.register(EntitiesMiddleware())
    dp.chat_join_request.outer_middleware.register(EntitiesMiddleware())
