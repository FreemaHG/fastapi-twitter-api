from pydantic import BaseModel
from http import HTTPStatus

class ResponseSchema(BaseModel):
    """
    Базовая схема для возврата успешного ответа
    """
    result: bool = True

    class Config:
        orm_mode = True

class ErrorResponseSchema(ResponseSchema):
    """
    Схема для неуспешного ответа с типом и текстом ошибки
    """
    result: bool = False
    error_type: str = HTTPStatus.NOT_FOUND
    error_message: str
