from datetime import timedelta

from app.data_structures.arq import JobConfig
from app.data_structures.captcha import LockJobKey
from app.services.scheduler import ArqScheduler


class CaptchaScheduler(ArqScheduler):
    async def enqueue_join_expire_job(
        self, target_id: str, captcha_duration: timedelta
    ) -> None:
        await self.enqueue_job(
            "join_expired_task",
            job_kwargs={"target_id": target_id},
            job_config=JobConfig(
                job_id=LockJobKey(target_id=target_id).pack(),
                run_after=captcha_duration,
            ),
        )

    async def abort_join_expire_job(self, target_id: str) -> None:
        lock_key = LockJobKey(target_id=target_id).pack()
        await self.abort_job(lock_key)
