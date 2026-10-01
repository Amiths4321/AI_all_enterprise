from app.evaluation.evidence import (
    SemanticEvidenceEvaluator,
)


def test_evidence_evaluator():

    documents = [
        {
            "id": "doc-1",
            "document": "Employees receive 20 days of annual leave.",
            "metadata": {
                "source": "hr_policy.txt"
            },
        }
    ]

    evaluator = SemanticEvidenceEvaluator()

    result = evaluator.evaluate(
        required_evidence=[
            "Employees receive 20 days of annual leave."
        ],
        retrieved_documents=documents,
    )

    assert "evidence_recall" in result
    assert "matches" in result
    assert len(result["matches"]) == 1