from app.retrieval.hybrid import HybridRetriever


def test_hybrid_retriever_keyword_search():

    documents = [
        {
            "id": "doc-1",
            "document": "Annual leave is 20 days.",
            "metadata": {"source": "hr_policy.txt"},
        },
        {
            "id": "doc-2",
            "document": "Employees receive health insurance.",
            "metadata": {"source": "benefits.txt"},
        },
    ]

    retriever = HybridRetriever(documents)

    results = retriever.retrieve(
        question="How many annual leave days?",
        top_k=2,
    )

    assert len(results) == 2
    assert results[0]["id"] == "doc-1"
    assert results[0]["metadata"]["source"] == "hr_policy.txt"