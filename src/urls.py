from fastapi import FastAPI
from routes.user import router as user_router
from routes.image import router as media_router
from routes.tweet import router as tweet_router


def register_routers(app: FastAPI) -> FastAPI:
    """
    Регистрация роутов для API
    """
    app.include_router(user_router)  # Вывод информации о пользователе
    app.include_router(media_router)  # Загрузка изображений к твитам
    app.include_router(tweet_router)  # Добавление, удаление и вывод твитов

    return app
