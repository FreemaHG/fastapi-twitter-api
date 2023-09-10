#!/bin/bash

# Запускаем gunicorn-сервер (с 4 воркерами) на 8000 порту (внутри контейнера)
uvicorn src.main:app
#gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000