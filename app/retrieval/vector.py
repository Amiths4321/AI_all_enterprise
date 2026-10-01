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

        self.embeddings = self.model.encode(
            [item["document"] for item in documents],
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

    def search(
        self,
        question: str,
        top_k: int = 10,
    ) -> list[dict[str, Any]]:

        query_embedding = self.model.encode(
            question,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        scores = cos_sim(
            query_embedding,
            self.embeddings,
        )[0]

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda index: float(scores[index]),
            reverse=True,
        )

        results = []

        for index in ranked_indexes[:top_k]:

            item = self.documents[index]

            results.append(
                {
                    "id": item["id"],
                    "document": item["document"],
                    "metadata": item.get("metadata", {}),
                    "score": float(scores[index]),
                }
            )

        return results