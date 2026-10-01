from typing import Any

from app.core.interfaces import (
    EvidenceEvaluator,
    Generator,
    Reranker,
    Retriever,
)


class RAGService:
    def __init__(
        self,
        retriever: Retriever,
        reranker: Reranker,
        evidence_evaluator: EvidenceEvaluator,
        generator: Generator,
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.evidence_evaluator = evidence_evaluator
        self.generator = generator

    def answer(
        self,
        question: str,
        required_evidence: list[str] | None = None,
        top_k: int = 10,
        top_n: int = 3,
    ) -> dict[str, Any]:

        retrieved = self.retriever.retrieve(
            question=question,
            top_k=top_k,
        )

        reranked = self.reranker.rerank(
            question=question,
            documents=retrieved,
            top_n=top_n,
        )

        evidence = self.evidence_evaluator.evaluate(
            required_evidence=required_evidence or [],
            retrieved_documents=reranked,
        )

        answer = self.generator.generate(
            question=question,
            documents=reranked,
        )

        return {
            "question": question,
            "answer": answer,
            "retrieved_documents": retrieved,
            "reranked_documents": reranked,
            "evidence": evidence,
        }