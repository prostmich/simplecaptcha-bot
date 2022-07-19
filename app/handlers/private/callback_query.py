from aiogram import Bot, Router, html
from aiogram.types import BufferedInputFile, CallbackQuery, InputMediaPhoto

from app.data_structures.callback_data import CaptchaAnswerCallbackData
from app.data_structures.captcha import CaptchaResultStatus
from app.misc.filename_utils import generate_captcha_image_filename
from app.misc.kb_generators import generate_chat_url_keyboard
from app.services.captcha import CaptchaService

router = Router()


@router.callback_query(CaptchaAnswerCallbackData.filter())
async def handle_captcha_answer(
    query: CallbackQuery,
    bot: Bot,
    callback_data: CaptchaAnswerCallbackData,
    captcha: CaptchaService,
) -> None:
    target_id = callback_data.target_id
    answer = callback_data.answer
    markup = None
    if not await captcha.is_captcha_target(target_id, query.from_user.id):
        text = "Капча уже недействительна"
        result_status = CaptchaResultStatus.FAILURE
    else:
        target_data = await captcha.get_target_data(target_id)
        if await captcha.is_correct_answer(target_id, answer):
            chat = await bot.get_chat(chat_id=target_data.chat_id)
            text = "Верно! Вы были допущены в чат {chat}".format(
                chat=html.bold(chat.title) if chat.title else ""
            )
            markup = (
                generate_chat_url_keyboard(chat.username) if chat.username else None
            )
            result_status = CaptchaResultStatus.SUCCESS
            await bot.approve_chat_join_request(
                chat_id=target_data.chat_id, user_id=target_data.user_id
            )
        else:
            text = "К сожалению ответ неверный. Попробуйте ещё раз позже."
            result_status = CaptchaResultStatus.FAILURE
            await bot.decline_chat_join_request(
                chat_id=target_data.chat_id, user_id=target_data.user_id
            )
    result_image = await captcha.get_captcha_result_image(result_status)
    image_filename = generate_captcha_image_filename(target_id, result_status)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=BufferedInputFile(result_image.getvalue(), filename=image_filename),
            caption=text,
        ),
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=markup,
    )
