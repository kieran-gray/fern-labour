from typing import Any

from keycloak import KeycloakAdmin, KeycloakGetError

from app.domain.user.entity import User
from app.domain.user.repository import UserRepository
from app.domain.user.vo_user_id import UserId


def keycloak_query_to_user(user_info: dict[str, Any]) -> User:
    def get_additional_attributes(
        metadata: dict[str, Any], attributes: list[str]
    ) -> dict[str, Any]:
        additional_attributes: dict[str, Any] = {}
        for attribute in attributes:
            if value := metadata.get(attribute):
                if isinstance(value, str):
                    additional_attributes[attribute] = value
                if isinstance(value, list):
                    additional_attributes[attribute] = value[0]
        return additional_attributes

    additional_attributes = get_additional_attributes(
        metadata=user_info.get("attributes", {}), attributes=["phone_number"]
    )
    return User(
        id_=UserId(user_info.get("id")),  # type: ignore
        username=user_info.get("username"),  # type: ignore
        email=user_info.get("email"),  # type: ignore
        first_name=user_info.get("firstName"),  # type: ignore
        last_name=user_info.get("lastName"),  # type: ignore
        phone_number=additional_attributes.get("phone_number"),
    )


class KeycloakUserRepository(UserRepository):
    def __init__(self, keycloak_admin: KeycloakAdmin) -> None:
        self._keycloak_admin = keycloak_admin

    async def save(self, user: User) -> None:
        raise NotImplementedError("user save not implemented")

    async def delete(self, user: User) -> None:
        raise NotImplementedError("user delete not implemented")

    async def get_by_id(self, user_id: UserId) -> User | None:
        try:
            user = await self._keycloak_admin.a_get_user(
                user_id=user_id.value, user_profile_metadata=True
            )
        except KeycloakGetError:
            return None
        return keycloak_query_to_user(user)

    async def get_by_ids(self, user_ids: list[UserId]) -> list[User]:
        users: list[User] = []
        for user_id in user_ids:
            try:
                user = await self._keycloak_admin.a_get_user(user_id.value)
                users.append(keycloak_query_to_user(user))
            except KeycloakGetError as e:
                print(f"Error fetching user with ID {user_id}: {e}")
        return users
