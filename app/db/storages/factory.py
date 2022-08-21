from sqlalchemy.ext.asyncio import AsyncSession

from app.db.storages.chat import ChatStorage


class StorageFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def chat(self):
        return ChatStorage(self.session)
