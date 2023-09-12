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
    error_type: str = HTTPStatus.NOT_FOUND  # 404 - не найден
    error_message: str = "Not found"

class UnauthorizedResponseSchema(ErrorResponseSchema):
    """
    Схема для неуспешного ответа при ошибке авторизации.
    Используется для вывода примера ответа в документации
    """
    error_type: str = HTTPStatus.UNAUTHORIZED  # 401 - не авторизован
    error_message: str = "User authorization error"

class ValidationResponseSchema(ErrorResponseSchema):
    """
    Схема для неуспешного ответа при ошибке валидации входных данных.
    Используется для вывода примера ответа в документации
    """
    error_type: str = HTTPStatus.UNPROCESSABLE_ENTITY  # 422 - не обрабатываемый запрос
    error_message: str = "Invalid input data"

class LockedResponseSchema(ErrorResponseSchema):
    """
    Схема для неуспешного ответа при блокировке действия.
    Используется для вывода примера ответа в документации
    """
    error_type: str = HTTPStatus.LOCKED  # 423 - заблокировано
    error_message: str = "The action is blocked"
