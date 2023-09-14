from itertools import chain
from typing import Dict, List
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

# from app.database import db
from models.tweets import Tweet
from models.users import User
from schemas.tweet import TweetInSchema
from services.image import ImageService
from utils.exeptions import CustomApiException


# from app.models.users import User
# from app.services.images import ImageService
# from app.utils.media import delete_images


class TweetsService:
    """
    Сервис для добавления, удаления и вывода твитов
    """

    # @classmethod
    # def get_tweets(cls, user: User) -> List[Tweet]:
    #     """
    #     Вывод последних твитов подписанных пользователей
    #     :param user: объект текущего пользователя
    #     :return: список с твитами
    #     """
    #
    #     tweets = db.session.execute(
    #         db.select(Tweet)
    #         .filter(Tweet.user_id.in_(user.id for user in user.following))
    #         .order_by(Tweet.created_at.desc())
    #     ).all()
    #
    #     # Очистка результатов от вложенных кортежей
    #     tweets = list(chain(*tweets))
    #
    #     return tweets

    @classmethod
    async def get_tweet(cls, tweet_id: int, session: AsyncSession) -> Tweet | None:
        """
        Получить твит по переданному id
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
        :param data: словарь с данными
        :return: объект нового твита
        """
        logger.debug("Добавление нового твита")

        # Сохраняем твит
        new_tweet = Tweet(tweet_data=tweet.tweet_data, user_id=current_user.id)
        session.add(new_tweet)
        # Фиксируем изменения, но не записываем в БД!!!
        await session.flush()

        # Сохраняем изображения, если есть
        tweet_media_ids = tweet.tweet_media_ids

        if tweet_media_ids and tweet_media_ids != []:
            # Привязываем изображения к твиту
            await ImageService.update_images(tweet_media_ids=tweet_media_ids, tweet_id=new_tweet.id, session=session)

        # Сохраняем в БД все изменения (новый твит и привязку картинок к твиту)
        await session.commit()

        return new_tweet


    @classmethod
    async def delete_tweet(cls, user: User, tweet_id: int, session: AsyncSession) -> None:
        """
        Удаление твита и его изображений
        :param user_id: id пользователя
        :param tweet_id: id удаляемого твита
        :return: None
        """
        logger.debug(f"Удаление твита")

        # Поиск твита по id
        tweet = await cls.get_tweet(tweet_id=tweet_id, session=session)

        if not tweet:
            logger.error("Твит не найден")

            raise CustomApiException(
                status_code=404,
                detail="Tweet not found"
            )

        else:
            logger.debug("Твит найден")

            if tweet.user_id != user.id:
                logger.error("Запрос на удаление чужого твита")

                raise CustomApiException(
                    status_code=423,
                    detail="The tweet that is being accessed is locked"
                )

            else:
                logger.debug("Удаление твита автором")

                # Удаляем изображения твита
                await ImageService.delete_images(tweet_id=tweet.id, session=session)

                # Удаляем твит
                await session.delete(tweet)
                await session.commit()
