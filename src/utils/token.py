from typing import Union, Optional, Dict, Any
from fastapi.security import APIKeyHeader
from starlette.requests import Request
from utils.exeptions import CustomApiException

class APITokenHeader(APIKeyHeader):
    """
    Класс для проверки и извлечения токена из header
    """
    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)

        if not api_key:
            if self.auto_error:
                # Кастомная ошибка для вывода сообщения в формате, указанном в документации
                raise CustomApiException(status_code=401, detail="User authorization error")
            else:
                return None

        return api_key

# Для авторизации в /docs (верхний правый угол)
TOKEN = APITokenHeader(name="api-key")
