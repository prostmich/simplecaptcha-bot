from typing import List, Set, Tuple, Union

from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import (
    CallbackQuery,
    Chat,
    ChatJoinRequest,
    ChatMemberUpdated,
    Message,
)
from pydantic import validator

ChatUpdate = Union[Message, CallbackQuery, Message, ChatJoinRequest, ChatMemberUpdated]
ChatTypeT = Union[str, List[str], Set[str], Tuple[str, ...]]
CHAT_TYPES: Set[str] = {"private", "group", "supergroup", "channel"}


class ChatType(BaseFilter):
    types: ChatTypeT

    @validator("types", pre=True)
    def pre_check_types(
        cls, value: ChatTypeT
    ) -> Union[List[str], Set[str], Tuple[str, ...]]:
        if isinstance(value, str):
            value = {value}
        if any(chat_type not in CHAT_TYPES for chat_type in value):
            raise ValueError("Unknown chat type")
        return value

    async def __call__(self, obj: ChatUpdate, event_chat: Chat) -> bool:
        if event_chat is None:
            # e.g. callback query in a message sent from inline mode
            return False
        return event_chat.type in self.types
