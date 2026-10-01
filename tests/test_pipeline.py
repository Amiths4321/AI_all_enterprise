from app.evaluation.evidence import SemanticEvidenceEvaluator
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.vector import InMemoryVectorSearcher
from app.retrieval.reranker import CrossEncoderReranker


def test_real_retrieval_pipeline():

    documents = [
        {
            "id": "hr-001",
            "document": "Employees receive 20 days of annual leave.",
            "metadata": {"source": "hr_policy.txt"},
        },
        {
            "id": "benefits-001",
            "document": "Employees receive health insurance.",
            "metadata": {"source": "benefits.txt"},
        },
        {
            "id": "leave-001",
            "document": "Annual leave requests must be submitted through HR.",
            "metadata": {"source": "leave_process.txt"},
        },
    ]

    vector_searcher = InMemoryVectorSearcher(
        documents=documents,
    )

    retriever = HybridRetriever(
        documents=documents,
        vector_searcher=vector_searcher,
    )

    retrieved = retriever.retrieve(
        question="How many annual leave days do employees receive?",
        top_k=3,
    )

    assert len(retrieved) == 3
    assert all("rrf_score" in item for item in retrieved)

    reranker = CrossEncoderReranker()

    reranked = reranker.rerank(
        question="How many annual leave days do employees receive?",
        documents=retrieved,
        top_n=2,
    )

    assert len(reranked) == 2
    assert all("rerank_score" in item for item in reranked)

    evaluator = SemanticEvidenceEvaluator()

    evidence = evaluator.evaluate(
        required_evidence=[
            "Employees receive 20 days of annual leave."
        ],
        retrieved_documents=reranked,
    )

    assert "evidence_recall" in evidence
    assert len(evidence["matches"]) == 1