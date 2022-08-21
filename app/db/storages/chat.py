from app.db.models.chat import Chat
from app.db.storages.base import BaseStorage


class ChatStorage(BaseStorage):
    async def create_chat(self, chat_id: int, has_permissions: bool) -> Chat:
        chat = Chat(id=chat_id, has_permissions=has_permissions)
        self.session.add(chat)
        await self.commit()
        return chat

    async def get_chat(self, chat_id: int) -> Chat:
        return await self.session.get(Chat, chat_id)

    async def change_lang(self, chat_id: int, lang: str) -> None:
        chat = await self.session.get(Chat, chat_id)
        if chat.lang != lang:
            chat.lang = lang
            await self.commit()

    async def change_permissions_status(
        self, chat_id: int, has_permissions: bool
    ) -> None:
        chat = await self.session.get(Chat, chat_id)
        if chat.has_permissions != has_permissions:
            chat.has_permissions = has_permissions
            await self.commit()
