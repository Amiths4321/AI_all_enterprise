from app.retrieval.hybrid import HybridRetriever
from app.retrieval.vector import InMemoryVectorSearcher
from app.retrieval.reranker import CrossEncoderReranker
from app.services.retrieval_service import (
    EnterpriseRetrievalService,
)


def test_enterprise_retrieval():

    documents = [
        {
            "id": "hr-001",
            "document": (
                "Employees receive 20 days "
                "of annual leave."
            ),
            "metadata": {
                "source": "hr.txt",
                "department": "HR",
                "document_type": "policy",
                "year": 2026,
            },
        },
        {
            "id": "finance-001",
            "document": (
                "The annual operating budget "
                "is reviewed by finance."
            ),
            "metadata": {
                "source": "finance.txt",
                "department": "Finance",
                "document_type": "policy",
                "year": 2026,
            },
        },
    ]

    vector_searcher = InMemoryVectorSearcher(
        documents
    )

    retriever = HybridRetriever(
        documents=documents,
        vector_searcher=vector_searcher,
    )

    reranker = CrossEncoderReranker()

    service = EnterpriseRetrievalService(
        retriever=retriever,
        reranker=reranker,
    )

    result = service.retrieve(
        question="What does the HR policy say about annual leave?",
        documents=documents,
        top_k=2,
        top_n=1,
    )

    assert result["filtered_count"] == 1
    assert len(
        result["retrieved_documents"]
    ) == 1

    assert (
        result["retrieved_documents"][0]["id"]
        == "hr-001"
    )

    assert len(
        result["reranked_documents"]
    ) == 1