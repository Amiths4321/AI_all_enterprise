from app.services.rag_service import RAGService

from tests.fakes import (
    FakeRetriever,
    FakeReranker,
    FakeEvidenceEvaluator,
    FakeGenerator,
)


def test_rag_service_orchestration():

    service = RAGService(
        retriever=FakeRetriever(),
        reranker=FakeReranker(),
        evidence_evaluator=FakeEvidenceEvaluator(),
        generator=FakeGenerator(),
    )

    result = service.answer(
        question="How many annual leave days are provided?"
    )

    assert result["question"] == (
        "How many annual leave days are provided?"
    )

    assert result["answer"] == "TEST ANSWER"

    assert len(
        result["retrieved_documents"]
    ) == 1

    assert len(
        result["reranked_documents"]
    ) == 1