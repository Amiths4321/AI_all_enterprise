from pathlib import Path
import json

from app.evaluation.retrieval_metrics import (
    recall_at_k,
    reciprocal_rank,
)


DATASET = Path("data/retrieval_golden.json")


def load_cases():
    return json.loads(
        DATASET.read_text(encoding="utf-8")
    )


def evaluate(
    cases,
    retriever,
    label,
):

    recalls = []
    reciprocal_ranks = []

    for case in cases:

        results = retriever.retrieve(
            case["question"],
            top_k=10,
        )

        ids = [
            document["id"]
            for document in results
        ]

        expected = case[
            "expected_document_ids"
        ]

        recalls.append(
            recall_at_k(
                ids,
                expected,
                10,
            )
        )

        reciprocal_ranks.append(
            reciprocal_rank(
                ids,
                expected,
            )
        )

    average_recall = (
        sum(recalls) / len(recalls)
        if recalls
        else 0.0
    )

    average_mrr = (
        sum(reciprocal_ranks)
        / len(reciprocal_ranks)
        if reciprocal_ranks
        else 0.0
    )

    print(
        f"{label}: "
        f"Recall@10={average_recall:.3f}, "
        f"MRR={average_mrr:.3f}"
    )


if __name__ == "__main__":
    print(
        "Use this script to compare the existing "
        "retriever against MultiQueryRRFRetriever."
    )