from typing import Any

from rank_bm25 import BM25Okapi

from app.core.interfaces import Retriever, VectorSearcher


class HybridRetriever(Retriever):

    def __init__(
        self,
        documents: list[dict[str, Any]],
        vector_searcher: VectorSearcher,
    ):
        self.documents = documents
        self.vector_searcher = vector_searcher

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return text.lower().split()

    @staticmethod
    def _matches_filters(
        item: dict[str, Any],
        filters: dict | None,
    ) -> bool:

        if not filters:
            return True

        metadata = item.get(
            "metadata",
            {},
        )

        for key, expected in filters.items():

            if expected is None:
                continue

            if metadata.get(key) != expected:
                return False

        return True

    def keyword_search(
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

        tokenized = [
            self._tokenize(item["document"])
            for item in eligible
        ]

        bm25 = BM25Okapi(tokenized)

        scores = bm25.get_scores(
            self._tokenize(question)
        )

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )

        results = []

        for index in ranked_indexes[:top_k]:

            item = eligible[index]

            results.append(
                {
                    "id": item["id"],
                    "document": item["document"],
                    "metadata": item.get(
                        "metadata",
                        {},
                    ),
                    "score": float(
                        scores[index]
                    ),
                }
            )

        return results

    def reciprocal_rank_fusion(
        self,
        vector_results,
        keyword_results,
        top_k=10,
        rrf_k=60,
    ):

        combined = {}

        for rank, item in enumerate(
            vector_results,
            start=1,
        ):

            document_id = item["id"]

            if document_id not in combined:
                combined[document_id] = {
                    "id": document_id,
                    "document": item["document"],
                    "metadata": item.get(
                        "metadata",
                        {},
                    ),
                    "vector_rank": None,
                    "keyword_rank": None,
                    "rrf_score": 0.0,
                }

            combined[document_id][
                "vector_rank"
            ] = rank

            combined[document_id][
                "rrf_score"
            ] += 1 / (rrf_k + rank)

        for rank, item in enumerate(
            keyword_results,
            start=1,
        ):

            document_id = item["id"]

            if document_id not in combined:
                combined[document_id] = {
                    "id": document_id,
                    "document": item["document"],
                    "metadata": item.get(
                        "metadata",
                        {},
                    ),
                    "vector_rank": None,
                    "keyword_rank": None,
                    "rrf_score": 0.0,
                }

            combined[document_id][
                "keyword_rank"
            ] = rank

            combined[document_id][
                "rrf_score"
            ] += 1 / (rrf_k + rank)

        return sorted(
            combined.values(),
            key=lambda item: item["rrf_score"],
            reverse=True,
        )[:top_k]

    def retrieve(
        self,
        question: str,
        top_k: int = 10,
        filters: dict | None = None,
        strategy: str = "hybrid",
    ) -> list[dict[str, Any]]:

        if strategy == "keyword":

            return self.keyword_search(
                question=question,
                top_k=top_k,
                filters=filters,
            )

        if strategy == "vector":

            return self.vector_searcher.search(
                question=question,
                top_k=top_k,
                filters=filters,
            )

        keyword_results = self.keyword_search(
            question=question,
            top_k=top_k,
            filters=filters,
        )

        vector_results = self.vector_searcher.search(
            question=question,
            top_k=top_k,
            filters=filters,
        )

        return self.reciprocal_rank_fusion(
            vector_results=vector_results,
            keyword_results=keyword_results,
            top_k=top_k,
        )