from app.retrieval.filters import MetadataFilter


def test_metadata_filter():

    documents = [
        {
            "id": "hr-1",
            "document": "HR policy",
            "metadata": {
                "department": "HR",
                "document_type": "policy",
                "year": 2026,
            },
        },
        {
            "id": "finance-1",
            "document": "Finance policy",
            "metadata": {
                "department": "Finance",
                "document_type": "policy",
                "year": 2026,
            },
        },
    ]

    filter_engine = MetadataFilter()

    result = filter_engine.apply(
        documents,
        department="HR",
        document_type="policy",
        year=2026,
    )

    assert len(result) == 1
    assert result[0]["id"] == "hr-1"