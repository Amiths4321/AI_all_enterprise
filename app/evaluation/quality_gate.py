from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationThresholds:

    min_recall_at_3: float = 0.80
    min_mrr: float = 0.70
    min_ndcg_at_3: float = 0.70

    min_answer_similarity: float = 0.70

    min_citation_precision: float = 0.90
    min_citation_recall: float = 0.80


class EvaluationQualityGate:

    def __init__(
        self,
        thresholds=None,
    ):

        self.thresholds = (
            thresholds
            or EvaluationThresholds()
        )

    def validate(
        self,
        result,
    ) -> dict:

        failures = []

        t = self.thresholds

        if result.recall_at_3 < t.min_recall_at_3:
            failures.append(
                "recall_at_3"
            )

        if result.mrr < t.min_mrr:
            failures.append("mrr")

        if result.ndcg_at_3 < t.min_ndcg_at_3:
            failures.append(
                "ndcg_at_3"
            )

        if (
            result.answer_similarity
            < t.min_answer_similarity
        ):
            failures.append(
                "answer_similarity"
            )

        if (
            result.citation_precision
            < t.min_citation_precision
        ):
            failures.append(
                "citation_precision"
            )

        if (
            result.citation_recall
            < t.min_citation_recall
        ):
            failures.append(
                "citation_recall"
            )

        if not result.security_passed:
            failures.append(
                "security"
            )

        return {
            "passed": len(failures) == 0,
            "failures": failures,
        }