from pydantic import BaseModel

from app.application.dtos.user import UserDTO
from app.application.dtos.user_summary import UserSummaryDTO


class UserResponse(BaseModel):
    user: UserDTO


class UserSummaryResponse(BaseModel):
    user: UserSummaryDTO


class UserListResponse(BaseModel):
    users: list[UserDTO]
