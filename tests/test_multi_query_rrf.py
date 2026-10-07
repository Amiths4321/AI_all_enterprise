from app.query.decomposer import QueryDecomposer
from app.query.entities import EntityExtractor
from app.query.intent import AdvancedIntentClassifier
from app.query.normalizer import QueryNormalizer
from app.query.planner import AdvancedQueryPlanner
from app.retrieval.multi_query_rrf import (
    MultiQueryRRFRetriever,
)
from app.retrieval.rrf import RRFFuser


class FakeRetriever:

    def retrieve(
        self,
        question,
        top_k=10,
        filters=None,
        strategy="hybrid",
    ):

        text = question.lower()

        if "policy" in text:
            return [
                {
                    "id": "hr-001",
                    "document": "Leave policy",
                },
                {
                    "id": "hr-002",
                    "document": "Leave procedure",
                },
            ]

        return [
            {
                "id": "hr-002",
                "document": "Leave procedure",
            },
            {
                "id": "hr-001",
                "document": "Leave policy",
            },
        ]


def build_planner():

    return AdvancedQueryPlanner(
        normalizer=QueryNormalizer(),
        intent_classifier=AdvancedIntentClassifier(),
        entity_extractor=EntityExtractor(),
        decomposer=QueryDecomposer(),
    )


def test_multi_query_rrf():

    pipeline = MultiQueryRRFRetriever(
        planner=build_planner(),
        retriever=FakeRetriever(),
        fuser=RRFFuser(),
    )

    results = pipeline.retrieve(
        "What is the leave policy and how do employees submit requests?"
    )

    assert len(results) == 2

    assert all(
        "rrf_score" in document
        for document in results
    )

    assert all(
        "retrieval_provenance" in document
        for document in results
    )