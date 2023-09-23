from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from loguru import logger

from src.models.likes import Like
from src.services.tweet import TweetsService
from src.utils.exeptions import CustomApiException

class LikeService:
    """
    Сервис для проставления лайков и дизлайков твитам
    """

    @classmethod
    async def like(cls, tweet_id: int, user_id: int, session: AsyncSession) -> None:
        """
        Лайк твита
        :param tweet_id: id твита для лайка
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: None
        """
        logger.debug(f"Лайк твита №{tweet_id}")

        # Поиск твита по id
        tweet = await TweetsService.get_tweet(tweet_id=tweet_id, session=session)

        if not tweet:
            logger.error("Твит не найден")

            raise CustomApiException(
                status_code=HTTPStatus.NOT_FOUND,  # 404
                detail="Tweet not found"
            )

        if await cls.check_like_tweet(tweet_id=tweet_id, user_id=user_id, session=session):
            logger.warning("Пользователь уже ставил лайк твиту")

            raise CustomApiException(
                status_code=HTTPStatus.LOCKED,  # 423
                detail="The user has already liked this tweet"
            )

        # TODO При реализации подсчета лайков
        # tweet.num_likes += 1  # Увеличиваем счетчик с лайками

        like_record = Like(user_id=user_id, tweets_id=tweet.id)

        session.add(like_record)
        await session.commit()

    @classmethod
    async def check_like_tweet(cls, tweet_id: int, user_id: int, session: AsyncSession) -> Like | None:
        """
        Проверка лайка (метод возвращает запись о лайке, проверяя тем самым, ставил ли пользователь лайк
        указанному твиту)
        :param tweet_id: id твита
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        """
        logger.debug("Поиск записи о лайке")

        query = select(Like).where(Like.user_id == user_id, Like.tweets_id == tweet_id)
        like = await session.execute(query)

        return like.scalar_one_or_none()

    @classmethod
    async def dislike(cls, tweet_id: int, user_id: int, session: AsyncSession) -> None:
        """
        Удаление лайка
        :param tweet_id: id твита
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: None
        """
        logger.debug(f"Дизлайк твита №{tweet_id}")

        # Поиск твита по id
        tweet = await TweetsService.get_tweet(tweet_id=tweet_id, session=session)

        if not tweet:
            logger.error("Твит не найден")

            raise CustomApiException(
                status_code=HTTPStatus.NOT_FOUND,  # 404
                detail="Tweet not found"
            )

        # Ищем запись о лайке
        like_record = await cls.check_like_tweet(tweet_id=tweet_id, user_id=user_id, session=session)

        logger.info(f"Найденный лайк: {like_record}")
        # logger.info(f"id: {like_record.id}")
        # logger.info(f"твит: {like_record.tweets_id}")
        # logger.info(f"автор: {like_record.user_id}")

        if like_record is None:
            logger.warning("Запись о лайке не найдена")

            raise CustomApiException(
                status_code=HTTPStatus.LOCKED,  # 423
                detail="The user has not yet liked this tweet"
            )

        await session.delete(like_record)  # Удаляем лайк

        # TODO Подсчет лайков
        # tweet.num_likes -= 1  # Уменьшаем счетчик лайков твита
        #
        # # Проверка, чтобы лайки не уходили в минус
        # if tweet.num_likes < 0:
        #     tweet.num_likes = 0

        await session.commit()
