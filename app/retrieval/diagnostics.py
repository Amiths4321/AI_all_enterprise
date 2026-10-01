from typing import Any


class RetrievalDiagnostics:

    def analyze(
        self,
        retrieved: list[dict[str, Any]],
        reranked: list[dict[str, Any]],
    ) -> dict[str, Any]:

        return {
            "retrieved_count": len(retrieved),
            "reranked_count": len(reranked),
            "retrieval_empty": len(retrieved) == 0,
            "reranking_empty": len(reranked) == 0,
            "retrieval_ids": [
                item["id"]
                for item in retrieved
            ],
            "reranked_ids": [
                item["id"]
                for item in reranked
            ],
        }