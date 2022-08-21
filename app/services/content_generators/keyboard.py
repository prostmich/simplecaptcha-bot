from typing import Set

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data_structures.callback_data import (
    CaptchaAnswerCallbackData,
    LangCallbackData,
)
from app.data_structures.captcha import Emoji
from app.services.content_generators.base import BaseContentGenerator

MAX_CAPTCHA_BUTTONS_ROW_LENGTH = 5


class KeyboardContentGenerator(BaseContentGenerator):
    def choose_lang(self, target: str) -> InlineKeyboardMarkup:
        language_titles = self.get_all("locale-title")
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=language_titles[lang],
                        callback_data=LangCallbackData(
                            lang_code=lang, target=target
                        ).pack(),
                    )
                ]
                for lang in language_titles
            ]
        )

    def go_to_chat(self, lang: str, chat_username: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=self.get_from("go-to-chat", locale=lang),
                        url=f"https://t.me/{chat_username}",
                    )
                ]
            ]
        )

    def invite_bot(self, bot_username: str, lang: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=self.get_from("invite-bot", locale=lang),
                        url=f"https://t.me/{bot_username}?startgroup=&admin=invite_users",
                    )
                ]
            ]
        )

    @staticmethod
    def captcha(
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
