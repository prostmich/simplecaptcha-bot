from aiogram import Router

from app.filters.chat_type import ChatType

from .callback_query import router as callback_query_router
from .message import router as message_router

router = Router()
router.callback_query.filter(ChatType(types="private"))
router.message.filter(ChatType(types="private"))

router.include_router(callback_query_router)
router.include_router(message_router)
