from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from app.services.content_generators.factory import ContentFactory

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, content_factory: ContentFactory) -> None:
    text = content_factory.text.choose_lang()
    markup = content_factory.keyboard.choose_lang(target="private_welcome_msg")
    await message.answer(text, reply_markup=markup)
