from aiogram import Router
from aiogram.types import Update

from app.misc.loggers import logger

router = Router()


@router.errors()
async def error_handler(update: Update, exception: Exception):
    exception_message = (
        exception.message if hasattr(exception, "message") else str(exception)
    )
    logger.exception(f"Caused error in update {update.json()}: {exception_message} ")
    return True
