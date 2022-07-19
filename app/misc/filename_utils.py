from typing import Optional

from app.data_structures.captcha import CaptchaResultStatus


def generate_captcha_image_filename(
    target_id: str, result_status: Optional[CaptchaResultStatus] = None
) -> str:
    filename = f"captcha_{target_id}"
    if result_status is not None:
        filename += f"_{result_status.name}"
    return f"{filename}.png"
