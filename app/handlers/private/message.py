from aiogram import Bot, Router
from aiogram.dispatcher.filters.command import Command, CommandStart
from aiogram.types import Message

from app.misc.kb_generators import generate_invite_bot_keyboard
from app.misc.settings_reader import Settings

router = Router()


@router.message(CommandStart())
async def handle_start_command(message: Message, bot: Bot) -> None:
    text = (
        "Привет! У вас есть проблема с ботами-спамерами в чате?\n"
        "У меня есть решение - captcha.\n\n"
        "Я буду проверять всех новые заявки в вашем чате на наличие спамеров.\n"
        "Для того, чтобы начать, выполните следующие действия:\n"
        "1. Перейдите в настройки чата и включите вступление по заявкам\n"
        "Тип чата > Заявки на вступление\n"
        "2. Нажмите на кнопку ниже, чтобы добавить меня в чат\n"
        "3. Следуйте моим дальнейшим инструкциям"
    )
    bot_user = await bot.get_me()
    markup = generate_invite_bot_keyboard(bot_username=bot_user.username)
    await message.answer(text, reply_markup=markup)


@router.message(Command(commands=["privacy"]))
async def handle_privacy_command(message: Message, settings: Settings) -> None:
    text = f"Privacy Policy:\n{settings.bot.privacy_policy_link}"
    await message.answer(text)
