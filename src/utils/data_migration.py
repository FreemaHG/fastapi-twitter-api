from loguru import logger

from src.database import async_session_maker
from src.models.users import User, user_to_user
from src.models.tweets import Tweet
from src.models.likes import Like

users = [
    {
        "id": 1,
        "username": "Дмитрий",
        "api-key": "user1",
    },
    {
        "id": 2,
        "username": "Елена",
        "api-key": "user2",
    },
    {
        "id": 3,
        "username": "Анастасия",
        "api-key": "user3",
    },
]

tweets = [
    {
        "id": 1,
        "tweet_data": "1 тестовый твит от Дмитрия",
        "user_id": 1,
    },
    {
        "id": 2,
        "tweet_data": "1 тестовый твит от Елены",
        "user_id": 2,
    },
    {
        "id": 3,
        "tweet_data": "1 тестовый твит от Анастасии",
        "user_id": 3,
    },
    {
        "id": 4,
        "tweet_data": "2 тестовый твит от Дмитрия",
        "user_id": 1,
    },
    {
        "id": 5,
        "tweet_data": "2 тестовый твит от Елены",
        "user_id": 2,
    },
    {
        "id": 6,
        "tweet_data": "3 тестовый твит от Елены",
        "user_id": 2,
    },
]

likes = [
    {
        "id": 1,
        "user_id": 1,
        "tweet_id": 1,
    },
    {
        "id": 2,
        "user_id": 2,
        "tweet_id": 2,
    },
    {
        "id": 3,
        "user_id": 3,
        "tweet_id": 1,
    },
    {
        "id": 4,
        "user_id": 1,
        "tweet_id": 3,
    },
    {
        "id": 5,
        "user_id": 2,
        "tweet_id": 1,
    },
    {
        "id": 6,
        "user_id": 1,
        "tweet_id": 2,
    },
    {
        "id": 7,
        "user_id": 3,
        "tweet_id": 2,
    },
    {
        "id": 8,
        "user_id": 2,
        "tweet_id": 3,
    },
]


async def migration_data():
    """
    Функция для наполнения БД данными
    """
    with async_session_maker as session:
        initial_users = [User(**user) for user in users]  # Инициализируем пользователей

        # Подписки пользователей
        initial_users[0].following.add(initial_users[1])
        initial_users[1].following.add(initial_users[0])
        initial_users[2].following.add(initial_users[1])

        initial_tweets = [Tweet(**tweet) for tweet in tweets]  # Инициализируем твиты
        initial_likes = [Like(**like) for like in likes]  # Инициализируем лайки

        # Добавляем и сохраняем данные в БД
        session.add_all(initial_users)
        session.add_all(initial_tweets)
        session.add_all(initial_likes)
        await session.commit()

        logger.debug('Данные загружены')
