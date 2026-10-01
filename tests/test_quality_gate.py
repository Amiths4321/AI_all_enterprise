from app.evaluation.quality_gate import (
    EvaluationQualityGate,
)
from app.evaluation.result import (
    EvaluationResult,
)


def test_quality_gate_passes():

    result = EvaluationResult(
        case_id="eval-001",
        recall_at_3=1.0,
        precision_at_3=1.0,
        mrr=1.0,
        ndcg_at_3=1.0,
        answer_similarity=0.95,
        citation_precision=1.0,
        citation_recall=1.0,
        citation_validity=1.0,
        security_passed=True,
        security_leakage_count=0,
    )

    result = EvaluationQualityGate().validate(
        result
    )

    assert result["passed"] is True
    assert result["failures"] == []


def test_quality_gate_rejects_security_failure():

    result = EvaluationResult(
        case_id="eval-001",
        recall_at_3=1.0,
        precision_at_3=1.0,
        mrr=1.0,
        ndcg_at_3=1.0,
        answer_similarity=0.95,
        citation_precision=1.0,
        citation_recall=1.0,
        citation_validity=1.0,
        security_passed=False,
        security_leakage_count=1,
    )

    result = EvaluationQualityGate().validate(
        result
    )

    assert result["passed"] is False
    assert "security" in result["failures"]