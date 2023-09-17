from typing import Optional
from http import HTTPStatus
from fastapi.security import APIKeyHeader
from starlette.requests import Request

from src.utils.exeptions import CustomApiException

class APITokenHeader(APIKeyHeader):
    """
    Проверка и извлечение токена из header
    """
    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)

        if not api_key:
            if self.auto_error:
                # Кастомная ошибка для вывода сообщения в формате, указанном в документации
                raise CustomApiException(
                    status_code=HTTPStatus.UNAUTHORIZED,  # 401
                    detail="User authorization error"
                )
            else:
                return None

        return api_key

# Для удобной авторизации в /docs (верхний правый угол на странице документации)
TOKEN = APITokenHeader(name="api-key")
