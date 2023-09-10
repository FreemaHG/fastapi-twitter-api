from pydantic import BaseModel
from http import HTTPStatus

class ResponseSchema(BaseModel):
    """
    Базовая схема для возврата успешного ответа
    """
    result: bool = True

    class Config:
        from_attributes = True

class ErrorResponseSchema(ResponseSchema):
    """
    Схема для неуспешного ответа с типом и текстом ошибки.
    Используется для вывода примера ответа в документации
    """
    result: bool = False
    error_type: str = HTTPStatus.NOT_FOUND
    error_message: str = "Not found"

class UnauthorizedResponseSchema(ErrorResponseSchema):
    """
    Схема для неуспешного ответа при ошибке авторизации.
    Используется для вывода примера ответа в документации
    """
    error_type: str = HTTPStatus.UNAUTHORIZED  # 401 - не авторизован
    error_message: str = "User authorization error"
