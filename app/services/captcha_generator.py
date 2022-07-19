import asyncio
import random
from io import BytesIO
from typing import List, Optional, Tuple

from app.data_structures.captcha import CaptchaData, CaptchaStaticData, Emoji, EmojiData
from app.misc.exceptions import CaptchaLoadError, FileOpenError
from app.misc.loggers import logger
from app.misc.paths import ASSETS_DIR

DEFAULT_CAPTCHA_BUTTONS_NUMBER = 10

MAPPING_FILE = ASSETS_DIR / "mapping.json"
IMG_DIR = ASSETS_DIR / "img"


class CaptchaGenerator:
    _all_emoji: Optional[List[EmojiData]] = None

    async def generate_captcha_data(
        self, buttons_number: int = DEFAULT_CAPTCHA_BUTTONS_NUMBER
    ) -> CaptchaData:
        if self._all_emoji is None:
            raise CaptchaLoadError("Emoji didn't loaded")
        try:
            correct_emoji, chosen_emoji = self._make_random_emoji_sequence(
                buttons_number
            )
            image = self.get_image(correct_emoji.code, "png")
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
            await self.generate_captcha_data(buttons_number)

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
    def get_image(filename: str, extension: str = "png") -> BytesIO:
        full_filename = f"{filename}.{extension}"
        try:
            with open(IMG_DIR / full_filename, "rb") as f:
                img = BytesIO()
                img.write(f.read())
                return img
        except OSError as e:
            logger.error(
                "Error on opening image file {filename}: {error!r}".format(
                    filename=full_filename,
                    error=e,
                ),
            )
            raise FileOpenError

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
