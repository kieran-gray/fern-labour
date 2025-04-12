from pydantic import BaseModel

from app.user.application.dtos.user import UserDTO
from app.user.application.dtos.user_summary import UserSummaryDTO


class UserResponse(BaseModel):
    user: UserDTO


class UserSummaryResponse(BaseModel):
    user: UserSummaryDTO


class UserListResponse(BaseModel):
    users: list[UserDTO]
