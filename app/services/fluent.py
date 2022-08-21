from pathlib import Path
from typing import Dict, Iterable, List, Optional

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub, TranslatorRunner

from app.data_structures.fluent import FluentLocale
from app.misc.exceptions import UnknownLanguageError

SUPPORTED_LOCALES = {"ru": "ru-RU", "en": "en-US"}
DEFAULT_LANGUAGE = "ru"
DEFAULT_LOCALE = SUPPORTED_LOCALES[DEFAULT_LANGUAGE]


class LocalesDataLoader:
    def __init__(self, locales_folder: Path) -> None:
        self.locales_folder = locales_folder

    def get_locales(self) -> List[FluentLocale]:
        locales = []
        for code, locale in SUPPORTED_LOCALES.items():
            locale_folder = self.locales_folder / code
            filenames = [
                str(filename)
                for filename in locale_folder.iterdir()
                if filename.suffix == ".ftl"
            ]
            locales.append(FluentLocale(code, locale, filenames))
        return locales


class FluentService:
    def __init__(
        self, locales_map: Dict[str, Iterable[str]], locales: Iterable[FluentLocale]
    ):
        self.locales_map = locales_map
        self.locales = locales
        self._hub: Optional[TranslatorHub] = None

    @property
    def hub(self) -> TranslatorHub:
        if not self._hub:
            self._hub = self._get_hub()
        return self._hub

    def _get_hub(self) -> TranslatorHub:
        return TranslatorHub(
            locales_map=self.locales_map,
            translators=[
                FluentTranslator(
                    locale=locale.code,
                    translator=FluentBundle.from_files(
                        locale=locale.code,
                        filenames=locale.filenames,
                        use_isolating=False,
                    ),
                )
                for locale in self.locales
            ],
            root_locale=DEFAULT_LANGUAGE,
        )

    def get_translator_by_locale(self, locale: str) -> TranslatorRunner:
        if locale not in SUPPORTED_LOCALES:
            raise UnknownLanguageError(f"Unknown locale: {locale}")
        return self.hub.get_translator_by_locale(locale)
