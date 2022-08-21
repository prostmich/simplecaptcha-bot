from aiogram import Bot, Router
from aiogram.types import BufferedInputFile, ChatJoinRequest

from app.db.models.chat import Chat
from app.misc.filename_utils import generate_captcha_image_filename
from app.services.captcha import CaptchaService
from app.services.content_generators.factory import ContentFactory

router = Router()


@router.chat_join_request()
async def handle_chat_join_request(
    update: ChatJoinRequest,
    bot: Bot,
    captcha: CaptchaService,
    content_factory: ContentFactory,
    chat: Chat,
) -> None:
    chat_id = update.chat.id
    user_id = update.from_user.id
    captcha_data = await captcha.generate_captcha(language=chat.lang)
    salt = await captcha.lock_user(
        chat_id, user_id, correct_code=captcha_data.correct_emoji_code
    )
    captcha_text = content_factory.text.captcha(chat_title=update.chat.title)

    captcha_kb = content_factory.keyboard.captcha(
        chat_id, user_id, salt, emoji_data=captcha_data.emoji_data
    )
    captcha_photo = BufferedInputFile(
        file=captcha_data.image.getvalue(),
        filename=generate_captcha_image_filename(chat_id, user_id),
    )
    await bot.send_photo(
        chat_id=user_id,
        photo=captcha_photo,
        caption=captcha_text,
        reply_markup=captcha_kb,
    )
