from sqlalchemy import BigInteger, Boolean, Column, String

from app.db.models.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id: int = Column(BigInteger, primary_key=True)
    lang: str = Column(String(2), default="ru")
    has_permissions: bool = Column(Boolean, default=False)
