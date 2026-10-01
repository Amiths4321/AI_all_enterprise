from app.evaluation.retrieval_metrics import (
    recall_at_k,
    precision_at_k,
    reciprocal_rank,
    ndcg_at_k,
)


def test_recall_at_3():

    assert recall_at_k(
        ["a", "b", "c"],
        ["b"],
        3,
    ) == 1.0


def test_precision_at_3():

    assert precision_at_k(
        ["a", "b", "c"],
        ["b"],
        3,
    ) == 1 / 3


def test_mrr():

    assert reciprocal_rank(
        ["a", "b", "c"],
        ["b"],
    ) == 0.5


def test_mrr_miss():

    assert reciprocal_rank(
        ["a", "b"],
        ["z"],
    ) == 0.0


def test_ndcg():

    score = ndcg_at_k(
        ["b", "a", "c"],
        ["b"],
        3,
    )

    assert score == 1.0