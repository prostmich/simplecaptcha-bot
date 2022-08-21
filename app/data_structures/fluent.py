from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class FluentLocale:
    code: str
    locale: str
    filenames: List[str]
