from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import List, NamedTuple, Set

from pydantic import BaseModel

from app.data_structures.redis import RedisBaseKey

Emoji = NamedTuple("Emoji", [("symbol", str), ("code", str)])


@dataclass
class CaptchaData:
    image: BytesIO
    correct_emoji_code: str
    emoji_data: Set[Emoji]


class CaptchaResultStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class EmojiData(BaseModel):
    symbol: str
    title: str
    code: str


class CaptchaStaticData(BaseModel):
    emoji: List[EmojiData]


class CaptchaRedisKeyPrefix(str):
    LOCK_JOB = "LOCK"
    ANSWER = "ANSWER"


@dataclass
class LockJobKey(RedisBaseKey):
    prefix = CaptchaRedisKeyPrefix.LOCK_JOB
    chat_id: int
    user_id: int
    salt: str


@dataclass
class AnswerKey(RedisBaseKey):
    prefix = CaptchaRedisKeyPrefix.ANSWER
    chat_id: int
    user_id: int
    salt: str
