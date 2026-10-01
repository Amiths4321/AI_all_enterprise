from app.retrieval.query_analyzer import (
    QueryAnalyzer,
)


def test_query_analysis():

    analyzer = QueryAnalyzer()

    result = analyzer.analyze(
        "What does the HR policy say about annual leave in 2026?"
    )

    assert result.department == "HR"
    assert result.document_type == "policy"
    assert result.year == 2026