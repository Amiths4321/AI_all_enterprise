from abc import ABC, abstractmethod
from typing import Any


class Retriever(ABC):
    @abstractmethod
    def retrieve(
        self,
        question: str,
        top_k: int = 10,
    ) -> list[dict[str, Any]]:
        pass


class Reranker(ABC):
    @abstractmethod
    def rerank(
        self,
        question: str,
        documents: list[dict[str, Any]],
        top_n: int = 3,
    ) -> list[dict[str, Any]]:
        pass


class EvidenceEvaluator(ABC):
    @abstractmethod
    def evaluate(
        self,
        required_evidence: list[str],
        retrieved_documents: list[dict[str, Any]],
    ) -> dict[str, Any]:
        pass


class Generator(ABC):
    @abstractmethod
    def generate(
        self,
        question: str,
        documents: list[dict[str, Any]],
    ) -> str:
        pass

class VectorSearcher(ABC):
    @abstractmethod
    def search(
        self,
        question: str,
        top_k: int = 10,
    ) -> list[dict[str, Any]]:
        pass