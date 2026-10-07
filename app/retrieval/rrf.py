from collections import defaultdict
from typing import Any


class RRFFuser:

    def __init__(self, k: int = 60):
        if k <= 0:
            raise ValueError("k must be positive")

        self.k = k

    def fuse(
        self,
        rankings: list[list[dict[str, Any]]],
        query_names: list[str] | None = None,
    ) -> list[dict[str, Any]]:

        scores = defaultdict(float)
        documents = {}
        provenance = defaultdict(list)

        if query_names is None:
            query_names = [
                f"query-{index + 1}"
                for index in range(len(rankings))
            ]

        if len(query_names) != len(rankings):
            raise ValueError(
                "query_names must match rankings"
            )

        for query_name, ranking in zip(
            query_names,
            rankings,
        ):

            for rank, document in enumerate(
                ranking,
                start=1,
            ):

                document_id = document["id"]

                scores[document_id] += (
                    1.0 / (self.k + rank)
                )

                documents[document_id] = document

                provenance[document_id].append(
                    {
                        "query": query_name,
                        "rank": rank,
                    }
                )

        fused = []

        for document_id, score in scores.items():

            document = dict(documents[document_id])

            document["rrf_score"] = score

            document["retrieval_provenance"] = (
                provenance[document_id]
            )

            fused.append(document)

        fused.sort(
            key=lambda document: document["rrf_score"],
            reverse=True,
        )

        return fused

def test_rrf_tracks_provenance():

    rankings = [
        [{"id": "A", "document": "A"}],
        [
            {"id": "B", "document": "B"},
            {"id": "A", "document": "A"},
        ],
    ]

    fuser = RRFFuser()

    result = fuser.fuse(
        rankings,
        query_names=["policy", "process"],
    )

    document_a = next(
        document
        for document in result
        if document["id"] == "A"
    )

    assert len(
        document_a["retrieval_provenance"]
    ) == 2