from typing import Set

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data_structures.callback_data import CaptchaAnswerCallbackData
from app.data_structures.captcha import Emoji

MAX_CAPTCHA_BUTTONS_ROW_LENGTH = 5


def generate_captcha_keyboard(
    chat_id: int, user_id: int, salt: str, emoji_data: Set[Emoji]
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for emoji in emoji_data:
        builder.add(
            InlineKeyboardButton(
                text=emoji.symbol,
                callback_data=CaptchaAnswerCallbackData(
                    chat_id=chat_id, user_id=user_id, salt=salt, answer=emoji.code
                ).pack(),
            )
        )
    builder.adjust(MAX_CAPTCHA_BUTTONS_ROW_LENGTH, repeat=True)
    return builder.as_markup()


def generate_invite_bot_keyboard(bot_username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Пригласить бота",
                    url=f"https://t.me/{bot_username}?startgroup=&admin=invite_users+delete_messages",
                )
            ]
        ]
    )


def generate_chat_url_keyboard(chat_username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Перейти в чат",
                    url=f"https://t.me/{chat_username}",
                )
            ]
        ]
    )
