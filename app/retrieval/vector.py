from typing import Any

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from app.core.interfaces import VectorSearcher


MODEL_NAME = "all-MiniLM-L6-v2"


class InMemoryVectorSearcher(VectorSearcher):

    def __init__(
        self,
        documents: list[dict[str, Any]],
        model_name: str = MODEL_NAME,
    ):
        self.documents = documents
        self.model = SentenceTransformer(model_name)

    @staticmethod
    def _matches_filters(
        item: dict[str, Any],
        filters: dict | None,
    ) -> bool:

        if not filters:
            return True

        metadata = item.get("metadata", {})

        for key, expected in filters.items():

            if expected is None:
                continue

            actual = metadata.get(key)

            if isinstance(expected, list):

                if actual not in expected:
                    return False

            elif actual != expected:
                return False

        return True

    def search(
        self,
        question: str,
        top_k: int = 10,
        filters: dict | None = None,
    ) -> list[dict[str, Any]]:

        eligible = [
            item
            for item in self.documents
            if self._matches_filters(
                item,
                filters,
            )
        ]

        if not eligible:
            return []

        document_embeddings = self.model.encode(
            [
                item["document"]
                for item in eligible
            ],
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        query_embedding = self.model.encode(
            question,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        scores = cos_sim(
            query_embedding,
            document_embeddings,
        )[0]

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda index: float(scores[index]),
            reverse=True,
        )

        results = []

        for index in ranked_indexes[:top_k]:

            item = eligible[index]

            results.append(
                {
                    "id": item["id"],
                    "document": item["document"],
                    "metadata": item.get("metadata", {}),
                    "score": float(scores[index]),
                }
            )

        return results