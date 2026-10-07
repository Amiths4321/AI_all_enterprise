from abc import ABC, abstractmethod


class Planner(ABC):

    @abstractmethod
    def plan(
        self,
        question: str,
    ) -> list[str]:
        raise NotImplementedError