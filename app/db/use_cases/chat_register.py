from app.db.models.chat import Chat
from app.db.use_cases.base import BaseUseCase


class ChatRegisterUseCase(BaseUseCase):
    async def get_or_create_chat(self, chat_id: int) -> Chat:
        chat_storage = self.storage_factory.chat
        if chat := await chat_storage.get_chat(chat_id):
            return chat
        return await chat_storage.create_chat(chat_id, has_permissions=False)
