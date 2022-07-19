from aiogram import Router

from app.filters.chat_type import ChatType

from .chat_join_request import router as chat_join_request_router
from .my_chat_member import router as my_chat_member_router

router = Router()
router.chat_join_request.filter(ChatType(types={"group", "supergroup"}))
router.my_chat_member.filter(ChatType(types={"group", "supergroup"}))

router.include_router(chat_join_request_router)
router.include_router(my_chat_member_router)
