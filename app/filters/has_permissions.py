from typing import List, Union

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Chat, Message
from cachetools import TTLCache
from pydantic import validator

EventObject = Union[CallbackQuery, Message]


class AdminCan(BaseFilter):
    permissions: Union[str, List[str]]
    _cache: TTLCache = TTLCache(maxsize=10_000, ttl=60)

    @validator("permissions")
    def extract_permissions(cls, v):
        if not isinstance(v, List):
            v = [v]
        return v

    async def _get_chat_member(self, obj: EventObject, chat: Chat, bot: Bot):
        cached_params: dict = self._cache.get(obj.from_user.id)
        if not cached_params:
            target_user_id = await self.get_target_id(obj, bot)
            chat_member = await bot.get_chat_member(chat.id, target_user_id)
            cached_params = chat_member.dict(
                exclude={"user", "custom_title", "until_date"}
            )
            self._cache[target_user_id] = cached_params
        return cached_params

    async def __call__(self, obj: EventObject, bot: Bot, event_chat: Chat) -> bool:
        if event_chat.type == "private":
            return True
        try:
            member: dict = await self._get_chat_member(obj, event_chat, bot)
        except TelegramAPIError:
            return False
        if member["status"] == "creator":
            return True
        if member["status"] != "administrator":
            return False
        if self.permissions == ["any"]:
            return True
        for permission in self.permissions:
            if not member.get(permission):
                return False
        return True

    async def get_target_id(self, obj: EventObject, bot: Bot):
        return obj.from_user.id


class BotCan(AdminCan):
    async def get_target_id(self, obj: EventObject, bot: Bot):
        return (await bot.me()).id
