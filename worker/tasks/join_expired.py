from typing import Any, Dict

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from app.misc.loggers import arq_logger as logger
from app.services.lock_user import LockUserService


async def join_expired_task(
    ctx: Dict[str, Any], chat_id: int, user_id: int, salt: str
) -> None:
    bot: Bot = ctx["bot"]
    lock_user: LockUserService = ctx["lock_user_service"]
    logger.info(
        "Checking if the user {user} in chat {chat} passed captcha".format(
            user=user_id, chat=chat_id
        )
    )
    is_captcha_passed = not await lock_user.is_captcha_target(chat_id, user_id, salt)
    if is_captcha_passed:
        logger.info(
            "The user user {user} in chat {chat} already pass captcha".format(
                user=user_id, chat=chat_id
            )
        )
        return
    try:
        await bot.decline_chat_join_request(chat_id, user_id)
        await lock_user.delete_correct_answer(chat_id, user_id, salt)
    except TelegramAPIError as e:
        logger.error(
            "Error while declining chat join request "
            "for user {user} in chat {chat}: {error}".format(
                user=user_id, chat=chat_id, error=e
            )
        )
        return
    logger.info(
        "The user ({user}) join request to chat ({chat}) "
        "was declined because of a captcha timeout".format(user=user_id, chat=chat_id)
    )
