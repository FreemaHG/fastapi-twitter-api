from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class Like(Base):
    """
    Модель для хранения данных о лайках к твитам
    """
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tweets_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"))

    # Отключаем проверку строк, тем самым убирая уведомление, возникающее при удалении несуществующей строки
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
