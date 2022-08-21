from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.types import Chat as TgChat
from aiogram.types import ChatJoinRequest, ChatMemberUpdated, Message, Update

from app.db.use_cases.chat_register import ChatRegisterUseCase

SupportedEvents = (Message, CallbackQuery, ChatMemberUpdated, ChatJoinRequest)


class EntitiesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        event_chat: TgChat = data["event_chat"]
        if isinstance(event, SupportedEvents) and event_chat.type != "private":
            use_case = ChatRegisterUseCase(storage_factory=data["storage_factory"])
            data["chat"] = await use_case.get_or_create_chat(chat_id=event_chat.id)
        return await handler(event, data)
