from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class Image(Base):
    """
    Модель для хранения данных об изображениях к твитам
    """
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), nullable=True)
    path_media: Mapped[str]

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
