from typing import Optional

from app.data_structures.captcha import AnswerKey
from app.services.redis import BaseRedis


class LockUserService(BaseRedis):
    def __init__(self, connection_uri: str):
        super().__init__(connection_uri)

    async def is_captcha_target(self, chat_id: int, user_id: int, salt: str) -> bool:
        answer_key = AnswerKey(chat_id, user_id, salt).pack()
        return bool(await self.redis.exists(answer_key))

    async def set_correct_answer(
        self, chat_id: int, user_id: int, salt: str, correct_code: str
    ) -> None:
        answer_key = AnswerKey(chat_id, user_id, salt).pack()
        await self.redis.set(answer_key, correct_code)

    async def get_correct_answer(
        self, chat_id: int, user_id: int, salt: str
    ) -> Optional[str]:
        answer_key = AnswerKey(chat_id, user_id, salt).pack()
        return await self.redis.get(answer_key)

    async def delete_correct_answer(
        self, chat_id: int, user_id: int, salt: str
    ) -> None:
        answer_key = AnswerKey(chat_id, user_id, salt).pack()
        await self.redis.delete(answer_key)
