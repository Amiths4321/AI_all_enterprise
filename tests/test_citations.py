from app.generation.citations import (
    CitationExtractor,
    CitationVerifier,
)


def test_extract_citations():

    answer = (
        "Employees receive 20 days "
        "of annual leave [1]."
    )

    result = CitationExtractor().extract(
        answer
    )

    assert result == [1]


def test_extract_multiple_citations():

    answer = (
        "Employees receive 20 days [1] "
        "and submit requests through the portal [2]."
    )

    result = CitationExtractor().extract(
        answer
    )

    assert result == [1, 2]


def test_duplicate_citations_are_removed():

    answer = (
        "The policy states this [1]. "
        "The same policy confirms it [1]."
    )

    result = CitationExtractor().extract(
        answer
    )

    assert result == [1]


def test_invalid_citation():

    documents = [
        type(
            "Document",
            (),
            {"number": 1},
        )()
    ]

    result = CitationVerifier().verify(
        "Some answer [99].",
        documents,
    )

    assert result["valid"] is False
    assert result["invalid_citations"] == [99]