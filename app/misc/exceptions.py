from typing import Any, Optional


class CustomException(Exception):
    def __init__(
        self,
        text: str = "",
        user_id: Optional[int] = None,
        chat_id: Optional[int] = None,
        *args: Optional[Any],
    ) -> None:
        super().__init__(text, args)
        self.text = text
        self.user_id = user_id
        self.chat_id = chat_id

    def __str__(self) -> str:
        text = f"{self.__class__.__name__}: {self.text}"
        if self.user_id is not None:
            text += f", by user {self.user_id} "
        if self.chat_id is not None:
            text += f"in chat {self.chat_id}"
        return text

    def __repr__(self) -> str:
        return str(self)


class FileOpenError(IOError, CustomException):
    def __init__(self, *args: Optional[Any]) -> None:
        super(CustomException).__init__(*args)


class CaptchaLoadError(ValueError, CustomException):
    def __init__(self, *args: Optional[Any]) -> None:
        super(CustomException).__init__(*args)
