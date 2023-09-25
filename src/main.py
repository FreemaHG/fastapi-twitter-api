from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from loguru import logger

from sqlalchemy.exc import ProgrammingError
from src.database import engine
from src.services.user import UserService
from src.utils.user import get_current_user
from src.utils.data_migrations import migration_data, re_creation_db
from src.urls import register_routers
from src.utils.exeptions import CustomApiException, custom_api_exception_handler


app = FastAPI(title="Twitter", debug=True, dependencies=[Depends(get_current_user)])

# Папка со статическим контентом
# app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

# Регистрация URL
register_routers(app)

# Регистрация кастомного исключения
app.add_exception_handler(CustomApiException, custom_api_exception_handler)

# FIXME Вынести миграции и добавлением демонстарционных данных в отдельную команду,
#  чтобы при запуске приложения каждый воркер не дублировал действия по проверке данных в БД
@app.on_event('startup')
async def shutdows():
    """
    Создаем и заполняем БД данными, если их нет
    """
    try:
        if not await UserService.check_users():
            logger.warning("В БД нет данных")
            await re_creation_db()  # Пересоздаем БД
            await migration_data()  # Загружаем первичные данные в БД

        else:
            logger.info("Имеются данные, запуск приложения без загрузки демонстрационных данных")

    except ProgrammingError:
        logger.error("БД не обнаружена")

        await re_creation_db()  # Пересоздаем БД
        await migration_data()  # Загружаем первичные данные в БД


@app.on_event('shutdown')
async def shutdows():
    """
    Закрываем сессию и соединение с БД
    """
    await engine.dispose()
