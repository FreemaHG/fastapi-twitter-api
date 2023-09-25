from loguru import logger
import asyncio

from src.database import async_session_maker, engine, Base
from src.models.users import User
from src.models.tweets import Tweet
from src.models.likes import Like
from src.models.images import Image


users = [
    {
        "username": "Дмитрий",
        "api_key": "test",
    },
    {
        "username": "Елена",
        "api_key": "test2",
    },
    {
        "username": "Анастасия",
        "api_key": "test3",
    },
]

images = [
    {
        "tweet_id": 1,
        "path_media": "images/tweets/migrations_img/1.jpeg",
    },
    {
        "tweet_id": 4,
        "path_media": "images/tweets/migrations_img/3.png",
    },
    {
        "tweet_id": 6,
        "path_media": "images/tweets/migrations_img/5.jpeg",
    },
    {
        "tweet_id": 6,
        "path_media": "images/tweets/migrations_img/7.jpeg",
    },
    {
        "tweet_id": 6,
        "path_media": "images/tweets/migrations_img/2.jpeg",
    },
    {
        "tweet_id": 8,
        "path_media": "images/tweets/migrations_img/4.png",
    },
    {
        "tweet_id": 11,
        "path_media": "images/tweets/migrations_img/6.jpeg",
    },
    {
        "tweet_id": 10,
        "path_media": "images/tweets/migrations_img/8.jpeg",
    },
]

tweets = [
    {
        "tweet_data": "Это я в ожидании своего отпуска )",
        "user_id": 1,
    },
    {
        "tweet_data": "Похоже снова придется наслаждаться конфетами",
        "user_id": 2,
    },
    {
        "tweet_data": "Кто сколько сбросил к Новому Году?",
        "user_id": 3,
    },
    {
        "tweet_data": "Очередной утомительный созвон на работе (((",
        "user_id": 2,
    },
    {
        "tweet_data": "Очаровательный получился подарок!!!",
        "user_id": 1,
    },
    {
        "tweet_data": "Предыдущий отпуск провели на отлично!",
        "user_id": 1,
    },
    {
        "tweet_data": "Кто знает, откуда это состояние?",
        "user_id": 3,
    },
    {
        "tweet_data": "Только посмотрите, кого я завела...",
        "user_id": 3,
    },
    {
        "tweet_data": "Интересно, почему чем больше денег, тем сумка кажется легче...",
        "user_id": 2,
    },
    {
        "tweet_data": "У меня тоже новый приятель )",
        "user_id": 2,
    },
    {
        "tweet_data": "Когда просишь у начальства зарплаты ))",
        "user_id": 2,
    },
    {
        "tweet_data": "Кто-нибудь уже приступил к квартальному отчету?",
        "user_id": 1,
    },
]

likes = [
    {
        "user_id": 1,
        "tweets_id": 1,
    },
    {
        "user_id": 3,
        "tweets_id": 1,
    },
    {
        "user_id": 2,
        "tweets_id": 1,
    },
    {
        "user_id": 2,
        "tweets_id": 2,
    },
    {
        "user_id": 3,
        "tweets_id": 2,
    },
    {
        "user_id": 1,
        "tweets_id": 3,
    },
    {
        "user_id": 2,
        "tweets_id": 3,
    },
    {
        "user_id": 1,
        "tweets_id": 4,
    },
    {
        "user_id": 1,
        "tweets_id": 6,
    },
    {
        "user_id": 3,
        "tweets_id": 6,
    },
    {
        "user_id": 2,
        "tweets_id": 7,
    },
    {
        "user_id": 1,
        "tweets_id": 9,
    },
    {
        "user_id": 2,
        "tweets_id": 9,
    },
    {
        "user_id": 2,
        "tweets_id": 11,
    },
    {
        "user_id": 3,
        "tweets_id": 11,
    },
]


async def re_creation_db():
    """
    Удаление и создание БД
    """
    logger.debug("Создание БД")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Удаление всех таблиц
        await conn.run_sync(Base.metadata.create_all)  # Создание всех таблиц


async def migration_data():
    """
    Функция для наполнения БД демонстрационными данными
    """
    logger.debug("Загрузка демонстрационных данных")

    await re_creation_db()

    async with async_session_maker() as session:
        # Инициализируем и добавляем пользователей
        initial_users = [User(**user) for user in users]
        session.add_all(initial_users)

        # Подписки пользователей
        initial_users[0].following.extend([initial_users[1], initial_users[2]])
        initial_users[1].following.append(initial_users[0])
        initial_users[2].following.extend([initial_users[1], initial_users[0]])

        # Твиты
        initial_tweets = [Tweet(**tweet) for tweet in tweets]
        session.add_all(initial_tweets)

        # Изображения к твитам
        initial_images = [Image(**image) for image in images]
        session.add_all(initial_images)

        # Лайки
        initial_likes = [Like(**like) for like in likes]
        session.add_all(initial_likes)

        await session.commit()

        logger.debug("Данные успешно добавлены")


if __name__ == "__main__":
    asyncio.run(migration_data())
