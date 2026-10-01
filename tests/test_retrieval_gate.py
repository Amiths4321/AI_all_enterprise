from app.evaluation.retrieval_gate import (
    RetrievalQualityGate,
)


def test_quality_gate_passes():

    gate = RetrievalQualityGate(
        minimum_recall_at_3=0.80,
        minimum_mrr=0.70,
    )

    result = gate.validate(
        recall_at_3=0.90,
        mrr=0.80,
    )

    assert result["passed"] is True


def test_quality_gate_fails():

    gate = RetrievalQualityGate(
        minimum_recall_at_3=0.80,
        minimum_mrr=0.70,
    )

    result = gate.validate(
        recall_at_3=0.50,
        mrr=0.40,
    )

    assert result["passed"] is False