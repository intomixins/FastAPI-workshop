from datetime import datetime

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from jose import (
    JWTError,
    jwt,
)

from passlib.hash import bcrypt

from pydantic import ValidationError

from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.auth import (
    Token,
    User,
    UserCreate,
)
from ..settings import settings


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={
                'WWW-Authenticate': 'Bearer',
            },
        )

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.from_orm(user)

        now = datetime.now()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + settings.jwt_expiration,
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=[settings.jwt_algorithm],
        )

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate) -> Token:
        user = tables.User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
        )

        self.session.add(user)
        self.session.commit()

        return self.create_token(user)
