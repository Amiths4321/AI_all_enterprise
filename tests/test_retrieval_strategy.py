from app.retrieval.intent import (
    IntentClassifier,
    QueryIntent,
)
from app.retrieval.strategy import (
    RetrievalStrategy,
    RetrievalStrategySelector,
)


def test_policy_query():

    classifier = IntentClassifier()

    intent = classifier.classify(
        "What is the annual leave policy?"
    )

    assert intent == QueryIntent.POLICY


def test_procedure_uses_keyword():

    selector = RetrievalStrategySelector()

    strategy = selector.select(
        QueryIntent.PROCEDURE
    )

    assert (
        strategy
        == RetrievalStrategy.KEYWORD
    )


def test_exploratory_uses_vector():

    selector = RetrievalStrategySelector()

    strategy = selector.select(
        QueryIntent.EXPLORATORY
    )

    assert (
        strategy
        == RetrievalStrategy.VECTOR
    )