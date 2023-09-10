from fastapi import FastAPI
from routes.user import router as user_router

def register_routers(app: FastAPI) -> FastAPI:
    """
    Регистрация роутов для API
    """
    app.include_router(user_router)  # Вывод информации о пользователе

    return app
