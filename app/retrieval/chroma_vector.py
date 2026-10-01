from typing import Any

from app.core.interfaces import VectorSearcher
from app.retrieval.chroma_repository import (
    ChromaDocumentRepository,
)


class ChromaVectorSearcher(VectorSearcher):

    def __init__(
        self,
        repository: ChromaDocumentRepository,
    ):
        self.repository = repository

    @staticmethod
    def _build_where(
        filters: dict | None,
    ) -> dict | None:

        if not filters:
            return None

        conditions = []

        for key, value in filters.items():

            if value is None:
                continue

            if isinstance(value, list):

                conditions.append(
                    {
                        key: {
                            "$in": value
                        }
                    }
                )

            else:

                conditions.append(
                    {
                        key: {
                            "$eq": value
                        }
                    }
                )

        if not conditions:
            return None

        if len(conditions) == 1:
            return conditions[0]

        return {
            "$and": conditions
        }

    def search(
        self,
        question: str,
        top_k: int = 10,
        filters: dict | None = None,
    ) -> list[dict[str, Any]]:

        where = self._build_where(
            filters
        )

        kwargs = {
            "query_texts": [question],
            "n_results": top_k,
        }

        if where:
            kwargs["where"] = where

        results = (
            self.repository.collection.query(
                **kwargs
            )
        )

        output = []

        for (
            document_id,
            document,
            metadata,
            distance,
        ) in zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):

            output.append(
                {
                    "id": document_id,
                    "document": document,
                    "metadata": metadata or {},
                    "score": (
                        1.0
                        - float(distance)
                    ),
                }
            )

        return output