from dataclasses import dataclass

from app.application.enums import ResponseStatusEnum


@dataclass(frozen=True, slots=True)
class DeleteOwnUserResponse:
    status: ResponseStatusEnum
