from app.query.decomposer import QueryDecomposer
from app.query.entities import EntityExtractor
from app.query.intent import AdvancedIntentClassifier
from app.query.normalizer import QueryNormalizer
from app.query.planner import AdvancedQueryPlanner


def build_planner():
    return AdvancedQueryPlanner(
        normalizer=QueryNormalizer(),
        intent_classifier=AdvancedIntentClassifier(),
        entity_extractor=EntityExtractor(),
        decomposer=QueryDecomposer(),
    )


def test_simple_question():

    planner = build_planner()

    plan = planner.plan(
        "How many annual leave days do employees receive?"
    )

    assert plan.normalized_question
    assert plan.sub_questions


def test_compound_question():

    planner = build_planner()

    plan = planner.plan(
        "What is the leave policy and how do employees submit requests?"
    )

    assert len(plan.sub_questions) == 2


def test_department_entity():

    planner = build_planner()

    plan = planner.plan(
        "What is the Finance budget policy?"
    )

    names = [entity.name for entity in plan.entities]

    assert "Finance" in names