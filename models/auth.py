from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserData(BaseModel):
    user_id: str
    username: str
    hashed_password: str


class UserTokenData(BaseModel):
    user_id: str


