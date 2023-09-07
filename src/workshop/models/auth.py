from pydantic import BaseModel


class BaseUser(BaseModel):
    """базовая модель пользователя."""
    email: str
    username: str


class UserCreate(BaseUser):
    """модель для создания пользователя."""
    password: str


class User(BaseUser):
    """модель для получения пользователя."""
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    """модель токена."""
    access_token: str
    token_type: str = 'bearer'
