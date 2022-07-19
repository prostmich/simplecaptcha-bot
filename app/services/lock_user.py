from typing import Optional

from app.data_structures.captcha import AnswerKey, LockTargetKey, TargetData
from app.misc.uuid import generate_uuid
from app.services.redis import BaseRedis


class LockUserService(BaseRedis):
    def __init__(self, connection_uri: str):
        super().__init__(connection_uri)

    async def store_target_data(self, chat_id: int, user_id: int) -> str:
        uuid = generate_uuid(length=20)
        target_key = LockTargetKey(target_id=uuid).pack()
        target_data = TargetData(chat_id=chat_id, user_id=user_id)
        await self.redis.set(target_key, str(target_data.json()))
        return uuid

    async def set_correct_answer(self, target_id: str, correct_code: str) -> None:
        answer_key = AnswerKey(target_id=target_id).pack()
        await self.redis.set(answer_key, correct_code)

    async def get_target_data(self, target_id: str) -> Optional[TargetData]:
        target_key = LockTargetKey(target_id=target_id).pack()
        data = await self.redis.get(target_key)
        if data:
            return TargetData.parse_raw(data)
        return None

    async def get_correct_answer(self, target_id: str) -> Optional[str]:
        answer_key = AnswerKey(target_id=target_id).pack()
        return await self.redis.get(answer_key)

    async def delete_target_data(self, target_id: str) -> None:
        target_key = LockTargetKey(target_id=target_id).pack()
        await self.redis.delete(target_key)

    async def delete_correct_answer(self, target_id: str) -> None:
        answer_key = AnswerKey(target_id=target_id).pack()
        await self.redis.delete(answer_key)
