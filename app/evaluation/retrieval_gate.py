from dataclasses import dataclass


@dataclass
class RetrievalQualityGate:

    minimum_recall_at_3: float = 0.80
    minimum_mrr: float = 0.70

    def validate(
        self,
        recall_at_3: float,
        mrr: float,
    ) -> dict:

        recall_passed = (
            recall_at_3
            >= self.minimum_recall_at_3
        )

        mrr_passed = (
            mrr
            >= self.minimum_mrr
        )

        return {
            "passed": (
                recall_passed
                and mrr_passed
            ),
            "recall_at_3": recall_at_3,
            "mrr": mrr,
            "recall_passed": recall_passed,
            "mrr_passed": mrr_passed,
        }