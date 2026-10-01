from app.evaluation.answer_metrics import (
    AnswerSimilarityEvaluator,
)


def test_similar_answers_have_high_similarity():

    evaluator = AnswerSimilarityEvaluator()

    score = evaluator.score(
        "Employees receive 20 days of annual leave.",
        "Employees receive 20 days of annual leave per year.",
    )

    assert score > 0.70