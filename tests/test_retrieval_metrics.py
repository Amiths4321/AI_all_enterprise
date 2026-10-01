from app.evaluation.retrieval_metrics import (
    recall_at_k,
    reciprocal_rank,
)


def test_recall_at_k():

    result = recall_at_k(
        retrieved_ids=[
            "wrong",
            "correct",
        ],
        expected_ids=[
            "correct",
        ],
        k=2,
    )

    assert result == 1.0


def test_reciprocal_rank():

    result = reciprocal_rank(
        retrieved_ids=[
            "wrong",
            "correct",
        ],
        expected_ids=[
            "correct",
        ],
    )

    assert result == 0.5