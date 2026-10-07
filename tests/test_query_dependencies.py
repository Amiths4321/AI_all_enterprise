from app.query.dependency_planner import (
    QueryDependencyPlanner,
)
from app.query.models import QueryPlan


def test_independent_questions():

    planner = QueryDependencyPlanner()

    plan = QueryPlan(
        original_question=(
            "What is the leave policy "
            "and how do I submit a request?"
        ),
        normalized_question=(
            "What is the leave policy "
            "and how do I submit a request?"
        ),
        sub_questions=[
            "What is the leave policy?",
            "How do I submit a request?",
        ],
    )

    nodes = planner.plan(plan)

    assert nodes[0].depends_on == []
    assert nodes[1].depends_on == []


def test_dependent_questions():

    planner = QueryDependencyPlanner()

    plan = QueryPlan(
        original_question=(
            "Who reviews the budget, "
            "and what happens after they approve it?"
        ),
        normalized_question=(
            "Who reviews the budget, "
            "and what happens after they approve it?"
        ),
        sub_questions=[
            "Who reviews the budget?",
            "What happens after they approve it?",
        ],
    )

    nodes = planner.plan(plan)

    assert nodes[0].depends_on == []
    assert nodes[1].depends_on == ["q1"]