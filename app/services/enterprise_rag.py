from typing import Any

from app.core.security import UserContext
from app.services.retrieval_service import EnterpriseRetrievalService
from app.services.grounded_answer import GroundedAnswerService


class EnterpriseRAGService:
    """
    Final application-level orchestration boundary.

    Responsibilities:
    - retrieve authorized evidence
    - enforce evidence sufficiency
    - generate grounded answer
    - verify citations/grounding
    """

    def __init__(
        self,
        retrieval_service: EnterpriseRetrievalService,
        grounded_answer_service: GroundedAnswerService,
    ):
        self.retrieval_service = retrieval_service
        self.grounded_answer_service = grounded_answer_service

    def answer(
        self,
        question: str,
        user: UserContext,
        top_k: int = 10,
        top_n: int = 3,
    ) -> dict[str, Any]:

        retrieval = self.retrieval_service.retrieve(
            question=question,
            user=user,
            top_k=top_k,
            top_n=top_n,
        )

        documents = retrieval.get("reranked_documents", [])

        if not documents:
            return {
                "question": question,
                "answer": (
                    "I cannot answer this question from the "
                    "authorized evidence available to you."
                ),
                "citations": [],
                "retrieval": retrieval,
                "grounded": False,
            }

        result = self.grounded_answer_service.answer(
            question=question,
            documents=documents,
        )

        return {
            "question": question,
            "answer": result["answer"],
            "citations": result.get("citations", []),
            "retrieval": retrieval,
            "grounded": result.get("grounded", False),
        }