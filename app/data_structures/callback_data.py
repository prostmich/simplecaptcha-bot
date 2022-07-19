from aiogram.dispatcher.filters.callback_data import CallbackData


class CaptchaAnswerCallbackData(CallbackData, prefix="captcha"):
    target_id: str
    answer: str
