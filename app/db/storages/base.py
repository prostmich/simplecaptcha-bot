from sqlalchemy.ext.asyncio import AsyncSession


class BaseStorage:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def begin(self):
        await self.session.begin()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()
