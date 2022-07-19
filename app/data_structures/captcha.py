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
    LOCK_TARGET = "LOCK_TARGET"


class TargetData(BaseModel):
    user_id: int
    chat_id: int


@dataclass
class LockJobKey(RedisBaseKey):
    prefix = CaptchaRedisKeyPrefix.LOCK_JOB
    target_id: str


@dataclass
class AnswerKey(RedisBaseKey):
    prefix = CaptchaRedisKeyPrefix.ANSWER
    target_id: str


@dataclass
class LockTargetKey(RedisBaseKey):
    prefix = CaptchaRedisKeyPrefix.LOCK_TARGET
    target_id: str
