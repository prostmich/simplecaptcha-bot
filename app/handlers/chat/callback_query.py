from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.data_structures.callback_data import LangCallbackData
from app.db.models.chat import Chat
from app.db.storages.factory import StorageFactory
from app.db.use_cases.chat_settings import ChatSettingsUseCase
from app.filters.has_permissions import AdminCan
from app.misc.exceptions import LanguageAlreadySetError, UnknownLanguageError
from app.services.content_generators.factory import ContentFactory

router = Router()


async def process_change_language(
    chat_id: int,
    lang: str,
    storage_factory: StorageFactory,
    content_factory: ContentFactory,
) -> str:
    use_case = ChatSettingsUseCase(storage_factory)
    try:
        await use_case.change_chat_lang(chat_id, lang)
    except LanguageAlreadySetError:
        get_content_method = content_factory.text.lang_change_already
    except UnknownLanguageError:
        get_content_method = content_factory.text.lang_change_bad_value
    else:
        get_content_method = content_factory.text.lang_change_success
    return get_content_method(lang=lang)


@router.callback_query(
    LangCallbackData.filter(F.target == "set_lang"), AdminCan(permissions="any")
)
async def change_language_due_to_set_lang(
    query: CallbackQuery,
    callback_data: LangCallbackData,
    content_factory: ContentFactory,
    storage_factory: StorageFactory,
) -> None:
    result_text = await process_change_language(
        chat_id=query.message.chat.id,
        lang=callback_data.lang_code,
        storage_factory=storage_factory,
        content_factory=content_factory,
    )
    await query.answer(text=result_text, show_alert=True)
    await query.message.delete()


@router.callback_query(
    LangCallbackData.filter(F.target == "group_welcome_msg"),
    AdminCan(permissions="any"),
)
async def change_language_due_to_group_welcome_msg(
    query: CallbackQuery,
    callback_data: LangCallbackData,
    content_factory: ContentFactory,
    storage_factory: StorageFactory,
    chat: Chat,
) -> None:
    result_text = await process_change_language(
        chat_id=query.message.chat.id,
        lang=callback_data.lang_code,
        storage_factory=storage_factory,
        content_factory=content_factory,
    )
    await query.answer(text=result_text, show_alert=True)
    text = content_factory.text.welcome_message(has_permissions=chat.has_permissions)
    await query.message.edit_text(text)


@router.callback_query(LangCallbackData.filter())
async def change_language_not_admin(
    query: CallbackQuery,
    content_factory: ContentFactory,
) -> None:
    text = content_factory.text.lang_change_not_admin()
    await query.answer(text=text, show_alert=True)
