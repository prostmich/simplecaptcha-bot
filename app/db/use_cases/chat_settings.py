from app.db.use_cases.base import BaseUseCase
from app.misc.exceptions import LanguageAlreadySetError, UnknownLanguageError
from app.services.fluent import DEFAULT_LANGUAGE, SUPPORTED_LOCALES


class ChatSettingsUseCase(BaseUseCase):
    async def change_chat_lang(self, chat_id: int, lang: str) -> None:
        if lang not in SUPPORTED_LOCALES:
            raise UnknownLanguageError(f"Unsupported language: {lang}", chat_id=chat_id)
        if lang == self.get_chat_lang(chat_id):
            raise LanguageAlreadySetError(
                f"Language already set to {lang}", chat_id=chat_id
            )
        await self.storage_factory.chat.change_lang(chat_id, lang)

    async def get_chat_lang(self, chat_id: int) -> str:
        chat = await self.storage_factory.chat.get_chat(chat_id)
        return chat.lang if chat else DEFAULT_LANGUAGE

    async def has_bot_permissions(self, chat_id: int) -> str:
        chat = await self.storage_factory.chat.get_chat(chat_id)
        return chat.has_permissions if chat else False

    async def set_bot_permissions_status(
        self, chat_id: int, has_permissions: bool
    ) -> None:
        await self.storage_factory.chat.change_permissions_status(
            chat_id, has_permissions
        )
