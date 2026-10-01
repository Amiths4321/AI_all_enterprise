from app.evaluation.citation_metrics import (
    citation_precision,
    citation_recall,
    citation_validity,
)


def test_citation_precision():

    assert citation_precision(
        ["hr-001"],
        ["hr-001"],
    ) == 1.0


def test_citation_recall():

    assert citation_recall(
        ["hr-001"],
        ["hr-001"],
    ) == 1.0


def test_citation_recall_partial():

    assert citation_recall(
        ["hr-001"],
        ["hr-001", "hr-002"],
    ) == 0.5


def test_invalid_citation():

    assert citation_validity(
        ["hr-999"],
        ["hr-001"],
    ) == 0.0