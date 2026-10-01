import math


def ndcg_at_k(
    retrieved_ids: list[str],
    expected_ids: list[str],
    k: int,
) -> float:

    retrieved = retrieved_ids[:k]
    expected = set(expected_ids)

    dcg = 0.0

    for index, document_id in enumerate(
        retrieved,
        start=1,
    ):
        relevance = (
            1
            if document_id in expected
            else 0
        )

        dcg += relevance / math.log2(
            index + 1
        )

    ideal_relevant = min(
        len(expected),
        k,
    )

    if ideal_relevant == 0:
        return 0.0

    idcg = sum(
        1 / math.log2(index + 1)
        for index in range(
            1,
            ideal_relevant + 1,
        )
    )

    return dcg / idcg
    
def precision_at_k(
    retrieved_ids: list[str],
    expected_ids: list[str],
    k: int,
) -> float:

    if k <= 0:
        return 0.0

    retrieved = retrieved_ids[:k]

    if not retrieved:
        return 0.0

    expected = set(expected_ids)

    relevant = sum(
        1
        for document_id in retrieved
        if document_id in expected
    )

    return relevant / len(retrieved)

def recall_at_k(
    retrieved_ids: list[str],
    expected_ids: list[str],
    k: int,
) -> float:

    if not expected_ids:
        return 1.0

    retrieved = set(
        retrieved_ids[:k]
    )

    expected = set(
        expected_ids
    )

    found = (
        retrieved
        .intersection(expected)
    )

    return (
        len(found)
        / len(expected)
    )
def reciprocal_rank(
    retrieved_ids: list[str],
    expected_ids: list[str],
) -> float:

    expected = set(expected_ids)

    for rank, document_id in enumerate(
        retrieved_ids,
        start=1,
    ):

        if document_id in expected:
            return 1.0 / rank

    return 0.0