from typing import Any

from rank_bm25 import BM25Okapi

from app.core.interfaces import Retriever, VectorSearcher


class HybridRetriever(Retriever):
    def __init__(
        self,
        documents,
        vector_searcher: VectorSearcher,
    ):
        self.documents = documents
        self.vector_searcher = vector_searcher

        tokenized_documents = [
            self._tokenize(item["document"])
            for item in documents
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return text.lower().split()

    def keyword_search(
        self,
        question: str,
        top_k: int = 10,
    ) -> list[dict[str, Any]]:

        query_tokens = self._tokenize(question)

        scores = self.bm25.get_scores(query_tokens)

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )

        results = []

        for index in ranked_indexes[:top_k]:
            candidate = self.documents[index]

            results.append(
                {
                    "id": candidate["id"],
                    "document": candidate["document"],
                    "metadata": candidate.get("metadata", {}),
                    "score": float(scores[index]),
                }
            )

        return results

    def reciprocal_rank_fusion(
        self,
        vector_results: list[dict[str, Any]],
        keyword_results: list[dict[str, Any]],
        top_k: int = 10,
        rrf_k: int = 60,
    ) -> list[dict[str, Any]]:

        combined: dict[str, dict[str, Any]] = {}

        for rank, item in enumerate(vector_results, start=1):

            document_id = item["id"]

            if document_id not in combined:
                combined[document_id] = {
                    "id": document_id,
                    "document": item["document"],
                    "metadata": item.get("metadata", {}),
                    "vector_rank": None,
                    "keyword_rank": None,
                    "rrf_score": 0.0,
                }

            combined[document_id]["vector_rank"] = rank

            combined[document_id]["rrf_score"] += (
                1 / (rrf_k + rank)
            )

        for rank, item in enumerate(keyword_results, start=1):

            document_id = item["id"]

            if document_id not in combined:
                combined[document_id] = {
                    "id": document_id,
                    "document": item["document"],
                    "metadata": item.get("metadata", {}),
                    "vector_rank": None,
                    "keyword_rank": None,
                    "rrf_score": 0.0,
                }

            combined[document_id]["keyword_rank"] = rank

            combined[document_id]["rrf_score"] += (
                1 / (rrf_k + rank)
            )

        results = sorted(
            combined.values(),
            key=lambda item: item["rrf_score"],
            reverse=True,
        )

        return results[:top_k]

    def retrieve(
        self,
        question: str,
        top_k: int = 10,
    ) -> list[dict[str, Any]]:

        keyword_results = self.keyword_search(
            question=question,
            top_k=top_k,
        )

        vector_results = self.vector_searcher.search(
            question=question,
            top_k=top_k,
        )

        return self.reciprocal_rank_fusion(
            vector_results=vector_results,
            keyword_results=keyword_results,
            top_k=top_k,
        )