import html

from app.services.content_generators.base import BaseContentGenerator


class TextContentGenerator(BaseContentGenerator):
    def welcome_message(self, has_permissions: bool) -> str:
        welcome_part = self.get("welcome")
        if has_permissions:
            permissions_part = self.get("welcome-permissions-have")
        else:
            permissions_part = self.get("welcome-permissions-missing")
        lang_changing_part = self.get("lang-changing-manual")
        return f"{welcome_part}\n\n{permissions_part}\n\n{lang_changing_part}"

    def bot_promoted(self, has_correct_permissions: bool) -> str:
        if has_correct_permissions:
            return self.get("bot-promoted-correct")
        else:
            return self.get("bot-promoted-incorrect")

    def bot_demoted(self) -> str:
        return self.get("bot-demoted")

    def captcha(self, chat_title: str) -> str:
        return self.get("captcha", chat=html.escape(chat_title))

    def lang_change_success(self, lang: str) -> str:
        return self.get_from(key="lang-change-success", locale=lang)

    def lang_change_already(self, lang: str) -> str:
        return self.get_from(key="lang-change-already", locale=lang)

    def lang_change_bad_value(self, lang: str) -> str:
        return self.get_from(key="lang-change-bad-value", locale=lang)

    def lang_change_not_admin(self) -> str:
        return self.get(key="lang-changing-not-admin")

    def captcha_invalid(self, lang: str) -> str:
        return self.get_from(key="captcha-invalid", locale=lang)

    def captcha_success(self, lang: str, chat_title: str) -> str:
        return self.get_from(
            key="captcha-success", locale=lang, chat=html.escape(chat_title)
        )

    def captcha_failure(self, lang: str) -> str:
        return self.get_from(key="captcha-failure", locale=lang)

    def choose_lang(self) -> str:
        rows = self.get_all(key="choose-lang").values()
        return "\n".join(rows)

    def start_manual(self, lang: str) -> str:
        return self.get_from(key="start-manual", locale=lang)
