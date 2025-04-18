from pydantic import BaseModel

from src.user.application.dtos.user import UserDTO
from src.user.application.dtos.user_summary import UserSummaryDTO


class UserResponse(BaseModel):
    user: UserDTO


class UserSummaryResponse(BaseModel):
    user: UserSummaryDTO


class UserListResponse(BaseModel):
    users: list[UserDTO]
