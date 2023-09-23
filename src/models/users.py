from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.tweets import Tweet
from src.models.likes import Like

# Подписки пользователей друг на друга
user_to_user = Table(
    "user_to_user",
    Base.metadata,
    Column("followers_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True),
)

class User(Base):
    """
    Модель для хранения данных о пользователях
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String(60), nullable=False, unique=True, index=True)
    api_key: Mapped[str] = mapped_column()
    # FIXME Вернуть, проверить работоспособность с шаблоном!
    # avatar: Mapped[str] = mapped_column(nullable=True)
    tweets: Mapped[List["Tweet"]] = relationship(backref="user", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(
        backref="user",
        cascade="all, delete-orphan",
    )

    # Подписки пользователей друг на друга (многие ко многим)
    following = relationship(
        "User",
        secondary=user_to_user,
        primaryjoin=id == user_to_user.c.followers_id,
        secondaryjoin=id == user_to_user.c.following_id,
        backref="followers",
        lazy="selectin",
    )

    # Отключаем проверку строк, тем самым убирая уведомление, возникающее при удалении несуществующей строки
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
