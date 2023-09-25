from loguru import logger

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
        "path_media": "images/tweets/migrations_img/avatar.jpg",
    },
    {
        "tweet_id": 2,
        "path_media": "images/tweets/migrations_img/Screen1.png",
    },
    {
        "tweet_id": 3,
        "path_media": "images/tweets/migrations_img/Screen2.png",
    },
    {
        "tweet_id": 1,
        "path_media": "images/tweets/migrations_img/stocks_1.png",
    },
]

tweets = [
    {
        "tweet_data": "1 тестовый твит от Дмитрия",
        "user_id": 1,
    },
    {
        "tweet_data": "1 тестовый твит от Елены",
        "user_id": 2,
    },
    {
        "tweet_data": "1 тестовый твит от Анастасии",
        "user_id": 3,
    },
    {
        "tweet_data": "2 тестовый твит от Дмитрия",
        "user_id": 1,
    },
    {
        "tweet_data": "2 тестовый твит от Елены",
        "user_id": 2,
    },
    {
        "tweet_data": "3 тестовый твит от Елены",
        "user_id": 2,
    },
]

likes = [
    {
        "user_id": 1,
        "tweets_id": 1,
    },
    {
        "user_id": 2,
        "tweets_id": 2,
    },
    {
        "user_id": 3,
        "tweets_id": 1,
    },
    {
        "user_id": 1,
        "tweets_id": 3,
    },
    {
        "user_id": 2,
        "tweets_id": 1,
    },
    {
        "user_id": 1,
        "tweets_id": 2,
    },
    {
        "user_id": 3,
        "tweets_id": 2,
    },
    {
        "user_id": 2,
        "tweets_id": 3,
    },
]


async def re_creation_db():
    """
    Удаление и создание БД
    """
    logger.debug("Удаление и создание БД")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Удаление всех таблиц
        await conn.run_sync(Base.metadata.create_all)  # Создание всех таблиц


async def migration_data():
    """
    Функция для наполнения БД демонстрационными данными
    """
    logger.debug("Загрузка демонстрационных данных")

    async with async_session_maker() as session:
        # Инициализируем и добавляем пользователей
        initial_users = [User(**user) for user in users]
        session.add_all(initial_users)

        # Подписки пользователей
        initial_users[0].following.append(initial_users[1])
        initial_users[1].following.append(initial_users[0])
        initial_users[2].following.append(initial_users[1])

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
