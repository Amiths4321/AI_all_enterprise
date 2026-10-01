from app.generation.grounding import (
    GroundingChecker,
)


def test_cited_answer_is_grounded():

    answer = (
        "Employees receive 20 days "
        "of annual leave [1]."
    )

    result = GroundingChecker().check(
        answer
    )

    assert result["grounded"] is True


def test_uncited_claim_is_detected():

    answer = (
        "Employees receive 20 days "
        "of annual leave [1]. "
        "Unused leave is automatically carried over."
    )

    result = GroundingChecker().check(
        answer
    )

    assert result["grounded"] is False
    assert len(
        result["uncited_sentences"]
    ) == 1