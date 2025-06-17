from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from settings import api_settings

from clients.aws import secrets_client, users_table

from models.auth import UserData, Token


SECRET_KEY = secrets_client.get_secret_value(api_settings.jwt_secret_key_name)["SecretString"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:

    @staticmethod
    def get_user_data(username: str) -> UserData:
        data = users_table.get_item(
            Key={
                "username": username
            },
        )

        return UserData(**data["Item"])

    @staticmethod
    def _verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def _get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(username: str, password: str):
        user = AuthService.get_user_data(username)
        if not user:
            return False
        if not AuthService._verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict) -> Token:
        to_encode = data.copy()
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=encoded_jwt, token_type="bearer")


    @staticmethod
    async def get_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            return user_id
        except InvalidTokenError:
            raise credentials_exception




