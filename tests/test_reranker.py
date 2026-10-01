from app.retrieval.reranker import CrossEncoderReranker


def test_reranker_returns_top_n():

    documents = [
        {
            "id": "doc-1",
            "document": "Annual leave is 20 days.",
            "metadata": {"source": "hr.txt"},
        },
        {
            "id": "doc-2",
            "document": "Employees receive health insurance.",
            "metadata": {"source": "benefits.txt"},
        },
    ]

    reranker = CrossEncoderReranker()

    results = reranker.rerank(
        question="How many annual leave days?",
        documents=documents,
        top_n=1,
    )

    assert len(results) == 1
    assert "rerank_score" in results[0]