from aiogram import Bot, F, Router
from aiogram.types import BufferedInputFile, CallbackQuery, InputMediaPhoto

from app.data_structures.callback_data import (
    CaptchaAnswerCallbackData,
    LangCallbackData,
)
from app.data_structures.captcha import CaptchaResultStatus
from app.db.storages.factory import StorageFactory
from app.db.use_cases.chat_settings import ChatSettingsUseCase
from app.misc.filename_utils import generate_captcha_image_filename
from app.services.captcha import CaptchaService
from app.services.content_generators.factory import ContentFactory

router = Router()


@router.callback_query(CaptchaAnswerCallbackData.filter())
async def handle_captcha_answer(
    query: CallbackQuery,
    bot: Bot,
    callback_data: CaptchaAnswerCallbackData,
    captcha: CaptchaService,
    content_factory: ContentFactory,
    storage_factory: StorageFactory,
) -> None:
    chat_id = callback_data.chat_id
    user_id = callback_data.user_id
    salt = callback_data.salt
    answer = callback_data.answer
    markup = None
    use_case = ChatSettingsUseCase(storage_factory)
    chat_lang = await use_case.get_chat_lang(chat_id)
    if not await captcha.is_captcha_target(chat_id, user_id, salt):
        text = content_factory.text.captcha_invalid(lang=chat_lang)
        result_status = CaptchaResultStatus.FAILURE
    else:
        if await captcha.is_correct_answer(chat_id, user_id, salt, answer):
            chat = await bot.get_chat(chat_id)
            text = content_factory.text.captcha_success(
                lang=chat_lang, chat_title=chat.title
            )
            markup = (
                content_factory.keyboard.go_to_chat(
                    lang=chat_lang, chat_username=chat.username
                )
                if chat.username
                else None
            )
            result_status = CaptchaResultStatus.SUCCESS
            await bot.approve_chat_join_request(chat_id, user_id)
        else:
            text = content_factory.text.captcha_failure(lang=chat_lang)
            result_status = CaptchaResultStatus.FAILURE
            await bot.decline_chat_join_request(chat_id, user_id)
        await captcha.unlock_user(chat_id, user_id, salt)
    result_image = await captcha.get_captcha_result_image(result_status)
    image_filename = generate_captcha_image_filename(chat_id, user_id, result_status)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=BufferedInputFile(result_image.getvalue(), filename=image_filename),
            caption=text,
        ),
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=markup,
    )


@router.callback_query(LangCallbackData.filter(F.target == "private_welcome_msg"))
async def handle_lang_callback(
    query: CallbackQuery,
    bot: Bot,
    callback_data: LangCallbackData,
    content_factory: ContentFactory,
) -> None:
    lang = callback_data.lang_code
    text = content_factory.text.start_manual(lang)
    bot_user = await bot.get_me()
    markup = content_factory.keyboard.invite_bot(
        bot_username=bot_user.username, lang=lang
    )
    await query.message.edit_text(text, reply_markup=markup)
