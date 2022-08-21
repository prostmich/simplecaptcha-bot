from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.orm import sessionmaker

from app.db.storages.factory import StorageFactory


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_maker: sessionmaker) -> None:
        self.session_maker = session_maker

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_maker() as session:
            data["session"] = session
            data["storage_factory"] = StorageFactory(session)
            return await handler(event, data)
