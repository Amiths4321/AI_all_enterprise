from app.evaluation.retrieval_failure import (
    RetrievalFailureAnalyzer,
)


def test_no_retrieval():

    analyzer = RetrievalFailureAnalyzer()

    result = analyzer.classify(
        retrieved_ids=[],
        expected_ids=["hr-001"],
    )

    assert result == "no_retrieval"


def test_retrieval_miss():

    analyzer = RetrievalFailureAnalyzer()

    result = analyzer.classify(
        retrieved_ids=["finance-001"],
        expected_ids=["hr-001"],
    )

    assert result == "miss"


def test_retrieval_success():

    analyzer = RetrievalFailureAnalyzer()

    result = analyzer.classify(
        retrieved_ids=["hr-001"],
        expected_ids=["hr-001"],
    )

    assert result == "success"