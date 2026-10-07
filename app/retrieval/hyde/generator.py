from abc import ABC, abstractmethod


class HypotheticalDocumentGenerator(ABC):

    @abstractmethod
    def generate(self, question: str) -> str:
        raise NotImplementedError