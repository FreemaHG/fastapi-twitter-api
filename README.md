# Описание проекта
Проект представляет собой backend-составляющую (API для twitter-подобного приложения) с возможностью постить твиты 
с картинками, ставить лайки, дизлайки, просматривать данные о себе и других пользователях, подписываться на других 
пользователей и просматривать ленту с твитами.

Предполагается, что у нас корпоративная сеть, а потому в сервисе нет возможности авторизации - 
аутентификация пользователей осуществляется через токен в header.

## Используемые инструменты
* Python (3.11);
* FastApi (asynchronous Wev Framework);
* Docker and Docker Compose (containerization);
* PostgreSQL (database);
* SQLAlchemy (working with database from Python);
* Alembic (database migrations made easy);
* Pydantic (data verification);
* Loguru (logging);
* Pytest (tests);
* Nginx (server for linking frontend and backend).

## Сборка и запуск приложения
1. Скачиваем содержимое репозитория в отдельную папку:
    ```
    git clone https://github.com/FreemaHG/fastapi_advanced_diploma.git
    ```
2. Переименовываем файл ".env.template" в ".env", при необходимости можно задать свои параметры.


3. Собираем и запускаем контейнеры с приложением. В терминале в общей директории (с файлом "docker-compose.yml") 
вводим команду:
    ```
    docker-compose up -d
    ```
4. Запускаем скрипт внутри контейнера с API для заполнения БД демонстрационными данными:
    ```
    docker-compose exec api python3 -m src.utils.data_migrations
    ```
В демонстрационных данных пользователи test, test2 и test3 уже подписаны друг на друга. 
Добавлены твиты с изображениями и лайки к записям.

## Документация

После сборки и запуска приложения ознакомиться с документацией API можно по адресу:
    ```
    <your_domain>/docs/
    ```

![](/screens/docs_1.png)
![](/screens/docs_2.png)
![](/screens/docs_3.png)

## Frontend

Для установки токена в header в правом верхнем углу frontend-ом предусмотрена форма для ввода api-key, 
по-умолчанию используется значение "test". После загрузки демонстрационны данных в БД будут сведения для 
пользователей с токенами "test", test2" и "test3". Все пользователи имеют данные с твитами, лайками и подписками.

![](/screens/front_1.png)
![](/screens/front_2.png)
![](/screens/front_3.png)
![](/screens/front_4.png)