import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from database import Base


class Tweet(Base):
    """
    Модель для хранения твитов
    """
    __tablename__ = "tweet"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    body: Mapped[str] = mapped_column(String(280))
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    images: Mapped[List["Media"]] = relationship(backref="tweet", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(backref="tweet", cascade="all, delete-orphan")
    num_kikes: Mapped[int] = mapped_column(default=0)
