from aiogram import Router

from .errors import router as errors_router

router = Router()
router.include_router(errors_router)
