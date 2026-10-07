import re


class QueryNormalizer:

    def normalize(self, question: str) -> str:
        question = question.strip()
        question = re.sub(r"\s+", " ", question)

        if not question:
            raise ValueError("Question cannot be empty")

        return question

from app.query.normalizer import QueryNormalizer


def test_query_normalizer():
    normalizer = QueryNormalizer()

    result = normalizer.normalize(
        "   How   many   leave days   do employees receive? "
    )

    assert result == (
        "How many leave days do employees receive?"
    )
    