from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import (
    CallbackQuery,
    ChatJoinRequest,
    ChatMemberUpdated,
    Message,
    Update,
)
from fluentogram import TranslatorRunner

from app.db.models.chat import Chat
from app.services.content_generators.factory import ContentFactory
from app.services.fluent import DEFAULT_LANGUAGE, FluentService

SupportedEvents = (Message, CallbackQuery, ChatMemberUpdated, ChatJoinRequest)


class LangMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, SupportedEvents):
            chat_lang: Chat = data["chat"].lang if "chat" in data else DEFAULT_LANGUAGE
            fluent: FluentService = data["fluent"]
            translator_runner: TranslatorRunner = fluent.get_translator_by_locale(
                locale=chat_lang
            )
            data["i18n"] = translator_runner
            data["i18n_hub"] = fluent.hub
            data["content_factory"] = ContentFactory(i18n=translator_runner)
        return await handler(event, data)
