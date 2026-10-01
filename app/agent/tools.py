from abc import ABC, abstractmethod


class AgentTool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        question: str,
        user,
    ) -> list[dict]:
        raise NotImplementedError