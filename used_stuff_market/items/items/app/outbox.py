import abc
from typing import Any
from pydantic import BaseModel


class Outbox(abc.ABC):
    @abc.abstractmethod
    def put(self, queue: str, message: BaseModel) -> None:
        pass
