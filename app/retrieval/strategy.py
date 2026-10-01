from enum import Enum

from app.retrieval.intent import QueryIntent


class RetrievalStrategy(str, Enum):

    KEYWORD = "keyword"
    VECTOR = "vector"
    HYBRID = "hybrid"


class RetrievalStrategySelector:

    def select(
        self,
        intent: QueryIntent,
    ) -> RetrievalStrategy:

        if intent == QueryIntent.PROCEDURE:
            return RetrievalStrategy.KEYWORD

        if intent == QueryIntent.EXPLORATORY:
            return RetrievalStrategy.VECTOR

        return RetrievalStrategy.HYBRID