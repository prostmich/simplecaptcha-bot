from fluentogram import TranslatorRunner

from app.services.content_generators.keyboard import KeyboardContentGenerator
from app.services.content_generators.text import TextContentGenerator


class ContentFactory:
    def __init__(self, i18n: TranslatorRunner):
        self.i18n = i18n

    @property
    def text(self):
        return TextContentGenerator(self.i18n)

    @property
    def keyboard(self):
        return KeyboardContentGenerator(self.i18n)
