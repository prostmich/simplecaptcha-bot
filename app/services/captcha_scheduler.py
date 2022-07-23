from datetime import timedelta

from app.data_structures.arq import JobConfig
from app.data_structures.captcha import LockJobKey
from app.services.scheduler import ArqScheduler


class CaptchaScheduler(ArqScheduler):
    async def enqueue_join_expire_job(
        self, chat_id: int, user_id: int, salt: str, captcha_duration: timedelta
    ) -> None:
        await self.enqueue_job(
            "join_expired_task",
            job_kwargs={"chat_id": chat_id, "user_id": user_id, "salt": salt},
            job_config=JobConfig(
                job_id=LockJobKey(chat_id=chat_id, user_id=user_id, salt=salt).pack(),
                run_after=captcha_duration,
            ),
        )

    async def abort_join_expire_job(
        self, chat_id: int, user_id: int, salt: str
    ) -> None:
        lock_key = LockJobKey(chat_id=chat_id, user_id=user_id, salt=salt).pack()
        await self.abort_job(lock_key)
