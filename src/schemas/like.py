from pydantic import BaseModel, Field, model_validator

from schemas.user import UserSchema

class LikeSchema(BaseModel):
    """
    Схема для вывода лайков при выводе твитов
    """
    id: int
    user_id: int
    user: UserSchema = Field(alias="name")  # Только поле name

    @model_validator(mode='before')
    def extract_user(cls, data):
        return vars(data["user"])
