from app.agent.executor import (
    AgentExecutor,
)
from app.agent.limits import (
    AgentLimits,
)
from app.core.security import (
    UserContext,
)


class FakePlanner:

    def plan(self, question):

        return [
            "leave policy",
            "leave request process",
        ]


class FakeTool:

    name = "enterprise_retrieval"

    def execute(
        self,
        question,
        user,
    ):

        if "policy" in question:
            return [
                {
                    "id": "hr-001",
                    "document": "20 days",
                }
            ]

        return [
            {
                "id": "hr-002",
                "document": "HR portal",
            }
        ]


def test_agent_executes_multiple_steps():

    executor = AgentExecutor(
        planner=FakePlanner(),
        tools=[FakeTool()],
        limits=AgentLimits(),
    )

    user = UserContext(
        "user-1",
        "employee",
        "HR",
    )

    state = executor.execute(
        "Tell me about leave",
        user,
    )

    assert state.completed is True

    assert len(
        state.sub_questions
    ) == 2

    assert len(
        state.steps
    ) == 2

    assert len(
        state.evidence
    ) == 2

def test_agent_respects_step_limit():

    class LargePlanner:

        def plan(self, question):
            return [
                "q1",
                "q2",
                "q3",
                "q4",
                "q5",
            ]

    executor = AgentExecutor(
        planner=LargePlanner(),
        tools=[FakeTool()],
        limits=AgentLimits(
            max_steps=2,
        ),
    )

    user = UserContext(
        "user-1",
        "employee",
        "HR",
    )

    state = executor.execute(
        "complex question",
        user,
    )

    assert state.completed is False
    assert (
        state.failure_reason
        == "step_limit_exceeded"
    )

def test_agent_rejects_too_many_sub_questions():

    class HugePlanner:

        def plan(self, question):
            return [
                f"question-{i}"
                for i in range(10)
            ]

    executor = AgentExecutor(
        planner=HugePlanner(),
        tools=[FakeTool()],
        limits=AgentLimits(
            max_sub_questions=3,
        ),
    )

    user = UserContext(
        "user-1",
        "employee",
        "HR",
    )

    state = executor.execute(
        "complex question",
        user,
    )

    assert state.completed is False
    assert (
        state.failure_reason
        == "too_many_sub_questions"
    )   