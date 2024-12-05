from abc import abstractmethod

from app.application.id_generator import IdGeneratorInterface


class SessionIdGeneratorInterface(IdGeneratorInterface[str]):
    @abstractmethod
    def __call__(self) -> str: ...
