from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from src.config import STATIC_FOLDER
from src.utils.user import get_current_user
from src.urls import register_routers
from src.utils.exeptions import CustomApiException, custom_api_exception_handler


# FIXME Используем глобальную зависимость - как не указывать в каждом ендпоинте (либо удалить от сюда)
app = FastAPI(title="Twitter", debug=True, dependencies=[Depends(get_current_user)])

# Задаем папку со статическим контентом
app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

# Регистрация URL
register_routers(app)

# Регистрация кастомного исключения
app.add_exception_handler(CustomApiException, custom_api_exception_handler)
