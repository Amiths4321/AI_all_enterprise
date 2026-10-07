from app.agent.rule_planner import (
    RuleBasedPlanner,
)


def test_simple_question():

    planner = RuleBasedPlanner()

    result = planner.plan(
        "What is the annual leave policy?"
    )

    assert result == [
        "What is the annual leave policy?"
    ]


def test_comparison_question():

    planner = RuleBasedPlanner()

    result = planner.plan(
        "annual leave policy vs production deployment policy"
    )

    assert len(result) == 2