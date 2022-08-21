from aiogram.filters.callback_data import CallbackData


class CaptchaAnswerCallbackData(CallbackData, prefix="captcha"):
    chat_id: int
    user_id: int
    salt: str
    answer: str
