from aiogram import Bot, Router, types
from aiogram.dispatcher.filters import (
    ADMINISTRATOR,
    JOIN_TRANSITION,
    KICKED,
    LEFT,
    MEMBER,
    RESTRICTED,
    ChatMemberUpdatedFilter,
)

router = Router()

NEED_PERMISSIONS = ("can_invite_users",)
PROMOTED_TRANSITION = (
    MEMBER | RESTRICTED | LEFT | KICKED | ADMINISTRATOR
) >> ADMINISTRATOR


def has_bot_need_permissions(member: types.ChatMember) -> bool:
    if not isinstance(member, types.ChatMemberAdministrator):
        return False
    return all(getattr(member, permission) for permission in NEED_PERMISSIONS)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
)
async def bot_joined(update: types.ChatMemberUpdated, bot: Bot) -> None:
    text = (
        "Привет! У вас есть проблема с ботами-спамерами в чате?\n"
        "У меня есть решение - captcha.\n\n"
    )
    if has_bot_need_permissions(update.new_chat_member):
        text += (
            "🎉 Я вижу, вы мне уже выдали нужные права администратора.\n"
            "Теперь я буду проверять всех новых участников на наличие спамеров."
        )
    else:
        text += (
            "😢 Я вижу, вы мне ещё не выдали нужные права администратора.\n"
            "К сожалению, без них я не смогу проверять новых участников на наличие спамеров.\n\n"
            "Права, которые мне нужны: \n"
            "👉 Пригласительные ссылки"
        )

    await bot.send_message(chat_id=update.chat.id, text=text)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=PROMOTED_TRANSITION),
)
async def bot_promoted(update: types.ChatMemberUpdated, bot: Bot) -> None:
    if has_bot_need_permissions(update.new_chat_member):
        text = (
            "🎉 Я получил нужные права администратора.\n"
            "Теперь я буду проверять новые заявки и отсеивать спамеров."
        )
    else:
        text = (
            "😢 Я получил не все нужные права администратора.\n"
            "К сожалению, без них я не смогу проверять новых заявки и отсеивать спамеров.\n\n"
            "Права, которые мне нужны: \n"
            "👉 Пригласительные ссылки"
        )
    await bot.send_message(chat_id=update.chat.id, text=text)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> MEMBER),
)
async def bot_demoted(update: types.ChatMemberUpdated, bot: Bot) -> None:
    text = (
        "😢 К сожалению, без прав администратора я не смогу проверять новых заявки "
        "и отсеивать спамеров.\n\n"
        "Права, которые мне нужны: \n"
        "👉 Пригласительные ссылки"
    )
    await bot.send_message(chat_id=update.chat.id, text=text)
