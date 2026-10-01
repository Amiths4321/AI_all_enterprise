from app.retrieval.diagnostics import (
    RetrievalDiagnostics,
)


def test_retrieval_diagnostics():

    diagnostics = RetrievalDiagnostics()

    result = diagnostics.analyze(
        retrieved=[
            {"id": "doc-1"},
            {"id": "doc-2"},
        ],
        reranked=[
            {"id": "doc-2"},
        ],
    )

    assert result["retrieved_count"] == 2
    assert result["reranked_count"] == 1
    assert result["retrieval_empty"] is False
    assert result["reranking_empty"] is False