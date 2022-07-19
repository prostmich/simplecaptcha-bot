from aiogram import Router

from .chat import router as chat_router
from .globals import router as global_router
from .private import router as private_router

main_router = Router()

main_router.include_router(chat_router)
main_router.include_router(global_router)
main_router.include_router(private_router)
