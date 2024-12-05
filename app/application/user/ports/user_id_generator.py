from abc import abstractmethod
from uuid import UUID

from app.application.id_generator import IdGeneratorInterface


class UserIdGeneratorInterface(IdGeneratorInterface[UUID]):
    @abstractmethod
    def __call__(self) -> UUID: ...
