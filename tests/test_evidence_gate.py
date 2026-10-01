from app.generation.evidence_gate import (
    EvidenceSufficiencyGate,
)


def test_empty_documents_are_insufficient():

    result = EvidenceSufficiencyGate().check([])

    assert result["sufficient"] is False


def test_documents_are_sufficient():

    documents = [
        {
            "id": "hr-001",
            "document": "Annual leave is 20 days.",
        }
    ]

    result = EvidenceSufficiencyGate().check(
        documents
    )

    assert result["sufficient"] is True