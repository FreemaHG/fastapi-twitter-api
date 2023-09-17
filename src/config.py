import os
from dotenv import load_dotenv

load_dotenv()  # Извлекаем переменные окружения из файла .env

STATIC_FOLDER = os.path.join(".", "src", "static")
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
