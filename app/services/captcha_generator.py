import asyncio
import random
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Tuple

from app.data_structures.captcha import CaptchaData, CaptchaStaticData, Emoji, EmojiData
from app.misc.exceptions import CaptchaLoadError, FileOpenError
from app.misc.loggers import logger
from app.misc.paths import RESOURCES_DIR

DEFAULT_CAPTCHA_BUTTONS_NUMBER = 10

MAPPING_FILE = RESOURCES_DIR / "mapping.json"
IMG_DIR = RESOURCES_DIR / "img"


class CaptchaGenerator:
    _all_emoji: Optional[List[EmojiData]] = None

    async def generate_captcha_data(
        self, language: str, buttons_number: int = DEFAULT_CAPTCHA_BUTTONS_NUMBER
    ) -> CaptchaData:
        if self._all_emoji is None:
            raise CaptchaLoadError("Emoji didn't loaded")
        try:
            images_folder = self.get_captcha_image_folder(language)
            correct_emoji, chosen_emoji = self._make_random_emoji_sequence(
                buttons_number
            )
            image = self.get_image(
                images_folder, filename=correct_emoji.code, extension="png"
            )
            chosen_emoji_data = {
                Emoji(emoji.symbol, emoji.code) for emoji in chosen_emoji
            }
            return CaptchaData(
                image=image,
                correct_emoji_code=correct_emoji.code,
                emoji_data=chosen_emoji_data,
            )
        except FileOpenError:
            await asyncio.sleep(0.1)
            await self.generate_captcha_data(language, buttons_number)

    def _make_random_emoji_sequence(
        self, total_number: int
    ) -> Tuple[EmojiData, List[EmojiData]]:
        if self._all_emoji is None:
            raise CaptchaLoadError("Emoji didn't loaded")
        chosen_emoji = random.sample(self._all_emoji, total_number)
        correct_emoji = chosen_emoji[0]
        random.shuffle(chosen_emoji)
        return correct_emoji, chosen_emoji

    @staticmethod
    def get_image(folder: Path, filename: str, extension: str = "png") -> BytesIO:
        full_path = folder / f"{filename}.{extension}"
        try:
            with open(full_path, "rb") as f:
                img = BytesIO()
                img.write(f.read())
                return img
        except OSError as e:
            logger.error(
                "Error on opening image file {full_path}: {error!r}".format(
                    full_path=full_path,
                    error=e,
                ),
            )
            raise FileOpenError

    @staticmethod
    def get_captcha_image_folder(language: str = "") -> Path:
        if language:
            return IMG_DIR / language
        return IMG_DIR

    @classmethod
    def load_emoji(cls) -> None:
        logger.debug("Loading emoji from JSON...")
        captcha_static_data: CaptchaStaticData = CaptchaStaticData.parse_file(
            MAPPING_FILE
        )
        logger.debug(
            "{number} emoji was loaded successfully".format(
                number=len(captcha_static_data.emoji)
            )
        )
        cls._all_emoji = captcha_static_data.emoji
