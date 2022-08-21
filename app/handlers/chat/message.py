from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.filters.has_permissions import AdminCan
from app.services.content_generators.factory import ContentFactory

router = Router()


@router.message(AdminCan(permissions="any"), Command(commands="lang"))
async def lang_command(message: Message, content_factory: ContentFactory) -> None:
    text = content_factory.text.choose_lang()
    markup = content_factory.keyboard.choose_lang(target="set_lang")
    await message.reply(text=text, reply_markup=markup)


@router.message(Command(commands="lang"))
async def lang_command_not_admin(
    message: Message,
    content_factory: ContentFactory,
) -> None:
    text = content_factory.text.lang_change_not_admin()
    await message.reply(text=text)
