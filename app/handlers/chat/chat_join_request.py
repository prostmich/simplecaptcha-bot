from aiogram import Bot, Router, html
from aiogram.types import BufferedInputFile, ChatJoinRequest

from app.misc.filename_utils import generate_captcha_image_filename
from app.misc.kb_generators import generate_captcha_keyboard
from app.services.captcha import CaptchaService

router = Router()


@router.chat_join_request()
async def handle_chat_join_request(
    update: ChatJoinRequest, bot: Bot, captcha: CaptchaService
) -> None:
    chat_id = update.chat.id
    user_id = update.from_user.id
    captcha_data = await captcha.generate_captcha()
    salt = await captcha.lock_user(
        chat_id, user_id, correct_code=captcha_data.correct_emoji_code
    )
    captcha_text = (
        "Привет 👋\n"
        "Ты отправил(а) заявку на вступление в чат {chat}.\n"
        "Но прежде чем я её одобрю, давай проверим, что ты действительно <b>человек</b>:\n"
        "Выбери <u>правильный вариант</u> в соответствии с заданием на картинке."
    ).format(chat=html.bold(update.chat.title) if update.chat.title else "")
    captcha_kb = generate_captcha_keyboard(
        chat_id, user_id, salt, emoji_data=captcha_data.emoji_data
    )
    captcha_photo = BufferedInputFile(
        file=captcha_data.image.getvalue(),
        filename=generate_captcha_image_filename(chat_id, user_id),
    )
    await bot.send_photo(
        user_id, photo=captcha_photo, caption=captcha_text, reply_markup=captcha_kb
    )
