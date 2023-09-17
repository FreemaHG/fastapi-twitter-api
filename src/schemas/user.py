from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

from src.schemas.base_response import ResponseSchema

class UserSchema(BaseModel):
    """
    Базовая схема для вывода основных данных о пользователе
    """
    id: int
    username: str = Field(alias="name")

    model_config = ConfigDict(
        from_attributes=True,  # Автоматическое преобразование данных ORM-модели в объект схемы для сериализации
        populate_by_name=True  # Использовать псевдоним вместо названия поля
    )

class UserDataSchema(UserSchema):
    """
    Схема для вывода детальной информации о пользователе
    """
    following: Optional[List["UserSchema"]] = []
    followers: Optional[List["UserSchema"]] = []

    # Автоматическое преобразование данных ORM-модели в объект схемы для сериализации
    model_config = ConfigDict(from_attributes=True)

class UserOutSchema(ResponseSchema):
    """
    Схема для вывода ответа с детальными данными о пользователе
    """
    user: UserDataSchema
