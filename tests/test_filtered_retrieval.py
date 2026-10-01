from app.retrieval.hybrid import HybridRetriever
from app.retrieval.vector import InMemoryVectorSearcher


def test_retrieval_respects_metadata_filter():

    documents = [
        {
            "id": "hr-1",
            "document": "HR annual leave policy.",
            "metadata": {
                "department": "HR",
                "document_type": "policy",
                "year": 2026,
            },
        },
        {
            "id": "finance-1",
            "document": "Finance annual budget policy.",
            "metadata": {
                "department": "Finance",
                "document_type": "policy",
                "year": 2026,
            },
        },
    ]

    vector = InMemoryVectorSearcher(
        documents
    )

    retriever = HybridRetriever(
        documents=documents,
        vector_searcher=vector,
    )

    results = retriever.retrieve(
        question="annual policy",
        top_k=10,
        filters={
            "department": "HR",
            "document_type": "policy",
            "year": 2026,
        },
    )

    assert len(results) == 1
    assert results[0]["id"] == "hr-1"