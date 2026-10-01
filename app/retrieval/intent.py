from enum import Enum


class QueryIntent(str, Enum):

    FACTUAL = "factual"
    POLICY = "policy"
    PROCEDURE = "procedure"
    EXPLORATORY = "exploratory"


class IntentClassifier:

    def classify(
        self,
        question: str,
    ) -> QueryIntent:

        lower = question.lower()

        if (
            "policy" in lower
            or "allowed" in lower
            or "permitted" in lower
        ):
            return QueryIntent.POLICY

        if (
            "how do" in lower
            or "how to" in lower
            or "procedure" in lower
            or "process" in lower
            or "steps" in lower
        ):
            return QueryIntent.PROCEDURE

        if (
            "overview" in lower
            or "explain" in lower
            or "tell me about" in lower
        ):
            return QueryIntent.EXPLORATORY

        return QueryIntent.FACTUAL