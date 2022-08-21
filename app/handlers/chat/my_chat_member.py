from aiogram import Bot, Router
from aiogram.filters import (
    ADMINISTRATOR,
    JOIN_TRANSITION,
    KICKED,
    LEAVE_TRANSITION,
    LEFT,
    MEMBER,
    RESTRICTED,
    ChatMemberUpdatedFilter,
)
from aiogram.types import ChatMember, ChatMemberAdministrator, ChatMemberUpdated

from app.db.models.chat import Chat
from app.db.storages.factory import StorageFactory
from app.db.use_cases.chat_settings import ChatSettingsUseCase
from app.services.content_generators.factory import ContentFactory

router = Router()

NEED_PERMISSIONS = ("can_invite_users",)
PROMOTED_TRANSITION = (
    MEMBER | RESTRICTED | LEFT | KICKED | ADMINISTRATOR
) >> ADMINISTRATOR


def has_bot_need_permissions(member: ChatMember) -> bool:
    if not isinstance(member, ChatMemberAdministrator):
        return False
    return all(getattr(member, permission) for permission in NEED_PERMISSIONS)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
)
async def bot_joined(
    update: ChatMemberUpdated,
    bot: Bot,
    content_factory: ContentFactory,
    storage_factory: StorageFactory,
) -> None:
    permissions_status = has_bot_need_permissions(update.new_chat_member)
    use_case = ChatSettingsUseCase(storage_factory)
    await use_case.set_bot_permissions_status(
        chat_id=update.chat.id, has_permissions=permissions_status
    )
    text = content_factory.text.choose_lang()
    markup = content_factory.keyboard.choose_lang(target="group_welcome_msg")
    await bot.send_message(chat_id=update.chat.id, text=text, reply_markup=markup)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=PROMOTED_TRANSITION),
)
async def bot_promoted(
    update: ChatMemberUpdated,
    bot: Bot,
    content_factory: ContentFactory,
    storage_factory: StorageFactory,
    chat: Chat,
) -> None:
    permissions_status = has_bot_need_permissions(update.new_chat_member)
    if chat.has_permissions == permissions_status:
        return
    use_case = ChatSettingsUseCase(storage_factory)
    await use_case.set_bot_permissions_status(
        chat_id=update.chat.id, has_permissions=permissions_status
    )
    text = content_factory.text.bot_promoted(has_correct_permissions=permissions_status)
    await bot.send_message(chat_id=update.chat.id, text=text)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> MEMBER),
)
async def bot_demoted(
    update: ChatMemberUpdated,
    bot: Bot,
    content_factory: ContentFactory,
    storage_factory: StorageFactory,
) -> None:
    use_case = ChatSettingsUseCase(storage_factory)
    await use_case.set_bot_permissions_status(
        chat_id=update.chat.id, has_permissions=False
    )
    text = content_factory.text.bot_demoted()
    await bot.send_message(chat_id=update.chat.id, text=text)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION),
)
async def bot_left(
    update: ChatMemberUpdated,
    storage_factory: StorageFactory,
) -> None:
    use_case = ChatSettingsUseCase(storage_factory)
    await use_case.set_bot_permissions_status(
        chat_id=update.chat.id, has_permissions=False
    )
