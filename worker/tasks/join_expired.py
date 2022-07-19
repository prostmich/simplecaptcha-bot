from typing import Any, Dict

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from app.misc.loggers import arq_logger as logger
from app.services.lock_user import LockUserService


async def join_expired_task(ctx: Dict[str, Any], target_id: str) -> None:
    bot: Bot = ctx["bot"]
    lock_user: LockUserService = ctx["lock_user_service"]
    logger.info(
        "Checking if the user with target_id {target_id} passed captcha".format(
            target_id=target_id,
        )
    )
    target_data = await lock_user.get_target_data(target_id)
    if not target_data:
        logger.info(
            "The user with target_id {target_id} from lock-list already pass captcha".format(
                target_id=target_id,
            )
        )
        return
    try:
        await bot.decline_chat_join_request(
            chat_id=target_data.chat_id, user_id=target_data.user_id
        )
        await lock_user.delete_target_data(target_id)
        await lock_user.delete_correct_answer(target_id)
    except TelegramAPIError as e:
        logger.error(
            "Error while declining chat join request "
            "for user with target_id {target_id}: {error}".format(
                target_id=target_id, error=e
            )
        )
    logger.info(
        "The user's ({user} join request to chat ({chat}) "
        "was declined because of a captcha timeout".format(
            user=target_data.user_id,
            chat=target_data.chat_id,
        )
    )
