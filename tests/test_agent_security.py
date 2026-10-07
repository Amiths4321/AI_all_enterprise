from app.agent.executor import (
    AgentExecutor,
)
from app.agent.limits import (
    AgentLimits,
)
from app.core.security import (
    UserContext,
)


class Planner:

    def plan(self, question):
        return [
            "What is the finance budget?"
        ]


class SecurityAwareRetrievalTool:

    name = "enterprise_retrieval"

    def execute(
        self,
        question,
        user,
    ):

        assert user.department == "HR"

        # Simulates the retrieval layer
        # already enforcing authorization.

        return []


def test_agent_cannot_bypass_user_context():

    executor = AgentExecutor(
        planner=Planner(),
        tools=[
            SecurityAwareRetrievalTool()
        ],
        limits=AgentLimits(),
    )

    user = UserContext(
        "employee-001",
        "employee",
        "HR",
    )

    state = executor.execute(
        "Tell me about finance",
        user,
    )

    assert state.completed is True
    assert state.evidence == []