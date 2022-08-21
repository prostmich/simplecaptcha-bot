from typing import Dict

from fluentogram import TranslatorRunner

from app.misc.exceptions import UnknownLanguageError


class BaseContentGenerator:
    def __init__(self, i18n: TranslatorRunner):
        self.i18n = i18n

    def get(self, key: str, **kwargs) -> str:
        return self.i18n.get(key, **kwargs)

    def get_from(self, key: str, locale: str, **kwargs) -> str:
        translator = next(filter(lambda t: t.locale == locale, self.i18n.translators))
        if not translator:
            raise UnknownLanguageError(f"No translator for locale {locale}")
        return translator.get(key, **kwargs)

    def get_all(self, key: str, **kwargs) -> Dict[str, str]:
        values_by_locales = {}
        for translator in self.i18n.translators:
            try:
                values_by_locales[translator.locale] = translator.get(key, **kwargs)
            except KeyError:
                pass
        return values_by_locales
