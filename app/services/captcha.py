import datetime
from io import BytesIO

from app.data_structures.captcha import CaptchaData, CaptchaResultStatus
from app.misc.uuid import generate_uuid
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

    async def is_captcha_target(self, chat_id: int, user_id: int, salt: str) -> bool:
        return await self._lock_service.is_captcha_target(chat_id, user_id, salt)

    async def is_correct_answer(
        self, chat_id: int, user_id: int, salt: str, answer: str
    ) -> bool:
        correct_code = await self._lock_service.get_correct_answer(
            chat_id, user_id, salt
        )
        return correct_code == answer

    async def lock_user(
        self,
        chat_id: int,
        user_id: int,
        correct_code: str,
    ) -> str:
        salt = generate_uuid(length=5)
        await self._lock_service.set_correct_answer(
            chat_id, user_id, salt, correct_code
        )
        await self._scheduler.enqueue_join_expire_job(
            chat_id, user_id, salt, captcha_duration=self._captcha_duration
        )
        return salt

    async def unlock_user(self, chat_id: int, user_id: int, salt: str) -> None:
        await self._lock_service.delete_correct_answer(chat_id, user_id, salt)
        await self._scheduler.abort_join_expire_job(chat_id, user_id, salt)
