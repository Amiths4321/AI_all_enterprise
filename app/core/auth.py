from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Identity:
    user_id: str
    role: str
    department: str


class Authenticator(ABC):

    @abstractmethod
    def authenticate(self, token: str) -> Identity:
        raise NotImplementedError