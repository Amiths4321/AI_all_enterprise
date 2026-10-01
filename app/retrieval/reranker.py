from typing import Any

from sentence_transformers import CrossEncoder

from app.core.interfaces import Reranker


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CrossEncoderReranker(Reranker):
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        question: str,
        documents: list[dict[str, Any]],
        top_n: int = 3,
    ) -> list[dict[str, Any]]:

        if not documents:
            return []

        pairs = [
            (question, item["document"])
            for item in documents
        ]

        scores = self.model.predict(pairs)

        results = []

        for item, score in zip(documents, scores):
            result = item.copy()
            result["rerank_score"] = float(score)
            results.append(result)

        results.sort(
            key=lambda item: item["rerank_score"],
            reverse=True,
        )

        return results[:top_n]