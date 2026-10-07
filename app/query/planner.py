from app.query.decomposer import QueryDecomposer
from app.query.entities import EntityExtractor
from app.query.intent import AdvancedIntentClassifier
from app.query.models import QueryPlan
from app.query.normalizer import QueryNormalizer


class AdvancedQueryPlanner:

    def __init__(
        self,
        normalizer: QueryNormalizer,
        intent_classifier: AdvancedIntentClassifier,
        entity_extractor: EntityExtractor,
        decomposer: QueryDecomposer,
    ):
        self.normalizer = normalizer
        self.intent_classifier = intent_classifier
        self.entity_extractor = entity_extractor
        self.decomposer = decomposer

    def plan(self, question: str) -> QueryPlan:

        normalized = self.normalizer.normalize(question)

        intents = self.intent_classifier.classify(
            normalized
        )

        entities = self.entity_extractor.extract(
            normalized
        )

        sub_questions = self.decomposer.decompose(
            normalized
        )

        return QueryPlan(
            original_question=question,
            normalized_question=normalized,
            intents=intents,
            entities=entities,
            sub_questions=sub_questions,
            retrieval_queries=sub_questions,
        )