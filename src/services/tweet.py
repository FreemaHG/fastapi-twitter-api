from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from loguru import logger

from src.models.likes import Like
from src.models.tweets import Tweet
from src.models.users import User
from src.services.image import ImageService
from src.utils.exeptions import CustomApiException
from src.schemas.tweet import TweetInSchema

class TweetsService:
    """
    Сервис для добавления, удаления и вывода твитов
    """

    @classmethod
    async def get_tweets(cls, user: User, session: AsyncSession):
        """
        Вывод последних твитов подписанных пользователей
        :param user: объект текущего пользователя
        :param session: объект асинхронной сессии
        :return: список с твитами
        """
        logger.debug("Вывод твитов")

        # FIXME По ТЗ возврат с сортировкой по популярности
        #  (сделать в модели подсчет лайков + сортировка по дате и лайкам)
        query = select(Tweet)\
            .filter(Tweet.user_id.in_(user.id for user in user.following))\
            .options(
                joinedload(Tweet.user),
                joinedload(Tweet.likes).subqueryload(Like.user),
                joinedload(Tweet.images),
            )\
            .order_by(Tweet.created_at.desc())
            # joinedload - запрашиваем данные из связанных таблиц
            # subqueryload - запрашиваем связанные вложенные данные по автору лайка без доп.запроса к БД

        result = await session.execute(query)
        tweets = result.unique().scalars().all()

        return tweets

    @classmethod
    async def get_tweet(cls, tweet_id: int, session: AsyncSession) -> Tweet | None:
        """
        Возврат твита по переданному id
        :param tweet_id: id твита для поиска
        :param session: объект асинхронной сессии
        :return: объект твита
        """
        logger.debug(f"Поиск твита по id: {tweet_id}")

        query = select(Tweet).where(Tweet.id == tweet_id)
        tweet = await session.execute(query)

        return tweet.scalar_one_or_none()

    @classmethod
    async def create_tweet(cls, tweet: TweetInSchema, current_user: User, session: AsyncSession) -> Tweet:
        """
        Создание нового твита
        :param tweet: данные для нового твита
        :param current_user: объект текущего пользователя
        :param session: объект асинхронной сессии
        :return: объект нового твита
        """
        logger.debug("Добавление нового твита")

        new_tweet = Tweet(tweet_data=tweet.tweet_data, user_id=current_user.id)

        # Добавляем в индекс, фиксируем, но не записываем в БД!!!
        session.add(new_tweet)
        await session.flush()

        # Сохраняем изображения, если есть
        tweet_media_ids = tweet.tweet_media_ids

        if tweet_media_ids and tweet_media_ids != []:
            # Привязываем изображения к твиту
            await ImageService.update_images(tweet_media_ids=tweet_media_ids, tweet_id=new_tweet.id, session=session)

        # Сохраняем в БД все изменения (новый твит + привязку картинок к твиту)
        await session.commit()

        return new_tweet


    @classmethod
    async def delete_tweet(cls, user: User, tweet_id: int, session: AsyncSession) -> None:
        """
        Удаление твита
        :param user: объект текущего пользователя
        :param tweet_id: id удаляемого твита
        :param session: объект асинхронной сессии
        :return: None
        """
        logger.debug(f"Удаление твита")

        # Поиск твита по id
        tweet = await cls.get_tweet(tweet_id=tweet_id, session=session)

        if not tweet:
            logger.error("Твит не найден")

            raise CustomApiException(
                status_code=HTTPStatus.NOT_FOUND,  # 404
                detail="Tweet not found"
            )

        else:
            if tweet.user_id != user.id:
                logger.error("Запрос на удаление чужого твита")

                raise CustomApiException(
                    status_code=HTTPStatus.LOCKED,  # 423
                    detail="The tweet that is being accessed is locked"
                )

            else:
                # Удаляем изображения твита
                await ImageService.delete_images(tweet_id=tweet.id, session=session)

                # Удаляем твит
                await session.delete(tweet)
                await session.commit()
