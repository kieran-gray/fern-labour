from pydantic import BaseModel

from app.application.base.enums import ResponseStatusEnum


class LogOutResponse(BaseModel):
    message: str


class LogInResponse(BaseModel):
    message: str


class SignUpResponse(BaseModel):
    username: str
    status: ResponseStatusEnum
