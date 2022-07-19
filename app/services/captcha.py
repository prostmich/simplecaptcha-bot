import datetime
from io import BytesIO
from typing import Optional

from app.data_structures.captcha import CaptchaData, CaptchaResultStatus, TargetData
from app.services.captcha_generator import CaptchaGenerator
from app.services.captcha_scheduler import CaptchaScheduler
from app.services.lock_user import LockUserService


class CaptchaService:
    def __init__(
        self,
        lock_service: LockUserService,
        scheduler: CaptchaScheduler,
        captcha_generator: CaptchaGenerator,
        captcha_duration: datetime.timedelta,
    ) -> None:
        self._lock_service = lock_service
        self._scheduler = scheduler
        self._captcha_duration = captcha_duration
        self._captcha_generator = captcha_generator

    async def generate_captcha(self) -> CaptchaData:
        return await self._captcha_generator.generate_captcha_data()

    async def get_captcha_result_image(self, status: CaptchaResultStatus) -> BytesIO:
        filename = f"captcha_{status.value}"
        return self._captcha_generator.get_image(filename, "png")

    async def is_captcha_target(self, target_id: str, user_id: int) -> bool:
        captcha_status = await self._lock_service.get_target_data(target_id)
        if captcha_status is None:
            return False
        return captcha_status.user_id == user_id

    async def is_correct_answer(self, target_id: str, answer: str) -> bool:
        correct_code = await self._lock_service.get_correct_answer(target_id)
        return correct_code == answer

    async def get_target_data(self, target_id: str) -> Optional[TargetData]:
        return await self._lock_service.get_target_data(target_id)

    async def lock_user(
        self,
        chat_id: int,
        user_id: int,
        correct_code: str,
    ) -> str:
        target_id = await self._lock_service.store_target_data(chat_id, user_id)
        await self._lock_service.set_correct_answer(target_id, correct_code)
        await self._scheduler.enqueue_join_expire_job(
            target_id, captcha_duration=self._captcha_duration
        )
        return target_id

    async def unlock_user(self, target_id: str) -> None:
        await self._lock_service.delete_target_data(target_id)
        await self._lock_service.delete_correct_answer(target_id)
        await self._scheduler.abort_join_expire_job(target_id)
