from app.query.decomposer import QueryDecomposer
from app.query.entities import EntityExtractor
from app.query.intent import AdvancedIntentClassifier
from app.query.normalizer import QueryNormalizer
from app.query.planner import AdvancedQueryPlanner
from app.retrieval.multi_query import MultiQueryRetriever


class FakeRetriever:

    def retrieve(
        self,
        question,
        top_k=10,
        filters=None,
        strategy="hybrid",
    ):
        if "leave policy" in question.lower():
            return [
                {
                    "id": "hr-001",
                    "document": "Employees receive 20 days of annual leave.",
                }
            ]

        return [
            {
                "id": "hr-002",
                "document": "Employees submit leave through the HR portal.",
            }
        ]


def build_planner():

    return AdvancedQueryPlanner(
        normalizer=QueryNormalizer(),
        intent_classifier=AdvancedIntentClassifier(),
        entity_extractor=EntityExtractor(),
        decomposer=QueryDecomposer(),
    )


def test_multi_query_deduplicates():

    retriever = MultiQueryRetriever(
        planner=build_planner(),
        retriever=FakeRetriever(),
    )

    documents = retriever.retrieve(
        "What is the leave policy and how do employees submit requests?"
    )

    ids = {document["id"] for document in documents}

    assert ids == {"hr-001", "hr-002"}