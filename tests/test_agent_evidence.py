from app.agent.evidence import (
    EvidenceAggregator,
)


def test_duplicate_documents_are_removed():

    aggregator = EvidenceAggregator()

    result = aggregator.aggregate(
        [
            [
                {
                    "id": "hr-001",
                    "document": "Leave policy",
                }
            ],
            [
                {
                    "id": "hr-001",
                    "document": "Leave policy",
                },
                {
                    "id": "hr-002",
                    "document": "Leave process",
                },
            ],
        ]
    )

    ids = [
        document["id"]
        for document in result
    ]

    assert ids == [
        "hr-001",
        "hr-002",
    ]