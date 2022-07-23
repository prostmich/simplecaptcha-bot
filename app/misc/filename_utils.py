from typing import Optional

from app.data_structures.captcha import CaptchaResultStatus


def generate_captcha_image_filename(
    chat_id: int, user_id: int, result_status: Optional[CaptchaResultStatus] = None
) -> str:
    filename = f"captcha_{chat_id}_{user_id}"
    if result_status is not None:
        filename += f"_{result_status.name}"
    return f"{filename}.png"
