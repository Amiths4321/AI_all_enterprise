from typing import Any


class RetrievalConfidenceEvaluator:

    def evaluate(
        self,
        documents: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not documents:
            return {
                "level": "none",
                "score": 0.0,
            }

        top_document = documents[0]

        score = top_document.get(
            "rerank_score",
            top_document.get(
                "rrf_score",
                top_document.get(
                    "score",
                    0.0,
                ),
            ),
        )

        score = float(score)

        if score >= 0.5:
            level = "high"

        elif score >= 0.1:
            level = "medium"

        else:
            level = "low"

        return {
            "level": level,
            "score": score,
        }