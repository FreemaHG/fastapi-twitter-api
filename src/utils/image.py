import os
import aiofiles

from http import HTTPStatus
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile
from loguru import logger

from models.images import Image
from config import ALLOWED_EXTENSIONS, IMAGES_FOLDER
from utils.exeptions import CustomApiException


def allowed_image(image_name: str) -> None:
    """
    Проверка расширения изображения
    :param image_name: название изображения
    :return: True - формат разрешен / False - формат не разрешен
    """
    logger.debug("Проверка формата изображения")

    # Проверяем, что расширение текущего файла есть в списке разрешенных
    # .rsplit('.', 1) - делит строку, начиная справа; 1 - делит 1 раз (по умолчанию -1 - неограниченное кол-во раз)
    if "." in image_name and image_name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
        logger.info("Формат изображения корректный")

    else:
        logger.error("Неразрешенный формат изображения")

        raise CustomApiException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,  # 422
            detail=f"The image has an unresolved format. You can only download the following formats: "
                   f"{', '.join(ALLOWED_EXTENSIONS)}"
        )


def clear_path(path: str) -> str:
    """
    Очистка входной строки от "static"
    :param path: строка - полный путь
    :return: очищенная строка
    """
    return path.split("static")[1][1:]


# FIXME Сделать сохранение в папку nginx/static
async def create_directory(path: str) -> None:
    """
    Создаем папку для сохранения изображений
    """
    logger.debug(f"Создание директории: {path}")
    os.makedirs(path)  # Создание нескольких вложенных папок


# FIXME Сделать добавление числового индекса в название файла при дублировании
# async def update_filename(filename: str) -> str:
#     """
#     Добавляем числовой индекс в название файла
#     :param filename: название файла
#     :return: обновленное название файла
#     """
#     count = 1
#     logger.debug(f"Старое название: {filename}")
#     new_filename = filename.replace(".", f"_{count}.")
#     logger.debug(f"Новое название: {new_filename}")
#     count+=1
#
#     return new_filename


async def save_image(file: UploadFile, avatar=False) -> str:
    """
    Сохранение изображения
    :param avatar: переключатель для сохранения аватара пользователя или изображения к твиту
    :param image: файл - изображение
    :return: путь относительно static для сохранения в БД
    """
    # Проверка формата загружаемого файла
    allowed_image(image_name=file.filename)

    with suppress(OSError):

        if avatar:
            logger.debug("Сохранение аватара пользователя")
            path = os.path.join(IMAGES_FOLDER, "avatars")

        else:
            logger.debug("Сохранение изображения к твиту")
            # Сохраняем изображения в директорию по дате добавления твита
            current_date = datetime.now()
            path = os.path.join(
                IMAGES_FOLDER,
                "tweets",
                f"{current_date.year}",
                f"{current_date.month}",
                f"{current_date.day}",
            )

        if not os.path.isdir(path):
            await create_directory(path=path)

        contents = file.file.read()
        full_path = os.path.join(path, f"{file.filename}")

        # FIXME Сделать добавление числового индекса в название файла при дублировании
        # Если файл с таким названием уже есть, то добавляем числовой индекс в название файла для сохранения
        # if os.path.isfile(full_path):
        #     new_file_name = await update_filename(filename=file.filename)
        #     full_path = os.path.join(path, f"{new_file_name}")

        # Сохраняем изображение
        async with aiofiles.open(full_path, mode="wb") as f:
            await f.write(contents)

        # Возвращаем очищенную строку для записи в БД
        return clear_path(path=full_path)


# FIXME Сделать при удалении твита
# def delete_images(tweet_id: int) -> None:
#     """
#     Удаление из файловой системы изображений по id твита
#     :param tweet_id: id твита
#     :return: None
#     """
#     logger.debug(f"Удаление изображений к твиту №{tweet_id}")
#
#     # Находим изображения по id твита
#     images = db.session.execute(
#         db.select(Image).filter(Image.tweet_id == tweet_id)
#     ).all()
#
#     if images:
#         images = list(chain(*images))  # Очищаем результат от вложенных кортежей
#         # Директория с изображениями к твиту
#         folder = os.path.join(
#             "static", images[0].path.rsplit("/", 1)[0].rsplit("\\", 1)[0]
#         )
#
#         for img in images:
#             try:
#                 os.remove(
#                     os.path.join("static", img.path)
#                 )  # Удаляем каждое изображение из файловой системы
#
#             except FileNotFoundError:
#                 logger.error(f"Директория: {img.path} не найдена")
#
#         logger.info("Все изображения удалены")
#
#         check_and_delete_folder(
#             path=folder
#         )  # Проверка и очистка директории, если пустая
#
#     else:
#         logger.warning("Изображения не найдены")
#
#
# def check_and_delete_folder(path: str) -> None:
#     """
#     Проверка и удаление папки, если пуста (подчистка пустых директорий после удаления твитов с изображениями)
#     :param path: директория с изображениями после удаления твита
#     :return: None
#     """
#     try:
#         # Удаляем папку, если пустая
#         if len(os.listdir(path)) == 0:
#             os.rmdir(path)
#             logger.info(f"Директория: {path} удалена")
#
#     except FileNotFoundError:
#         logger.error(f"Директория: {path} не найдена")
