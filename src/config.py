import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Извлекаем переменные окружения из файла .env


BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_FOLDER = os.path.join(".", "nginx", "static")
IMAGES_FOLDER = os.path.join(STATIC_FOLDER, "images")

# Разрешенные форматы изображений для загрузки
ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
    }

# PostgresSQL
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


# # 2 вариант подгрузки и использования переменных окружения
# from pydantic import BaseSettings, SettingsConfigDict
#
# class Settings(BaseSettings):
#
#     # Аннотация типов для проверки и валидации данных
#     MODE: str
#
#     DB_HOST: str
#     DB_PORT: int
#     DB_USER: str
#     DB_PASS: str
#     DB_NAME: str
#
#     @property
#     def DB_URL(self):
#         return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
#
#     # Подгружаем переменные окружения из файла
#     model_config = SettingsConfigDict(env_file=".env")
#
# # Сохраняем все в переменную для доступа в других файлах
# settings = Settings()
