from app.agent.state import (
    AgentState,
    AgentStep,
)
from app.agent.evidence import (
    EvidenceAggregator,
)


class AgentExecutor:

    def __init__(
        self,
        planner,
        tools,
        limits,
    ):
        self.planner = planner
        self.tools = {
            tool.name: tool
            for tool in tools
        }
        self.limits = limits

        self.evidence_aggregator = (
            EvidenceAggregator()
        )

    def execute(
        self,
        question,
        user,
    ):

        state = AgentState(
            original_question=question
        )

        sub_questions = self.planner.plan(
            question
        )

        if not sub_questions:
            state.failure_reason = (
                "planner_returned_no_questions"
            )
            return state

        if len(sub_questions) > (
            self.limits.max_sub_questions
        ):
            state.failure_reason = (
                "too_many_sub_questions"
            )
            return state

        state.sub_questions = (
            sub_questions
        )

        evidence_sets = []

        for index, sub_question in enumerate(
            sub_questions,
            start=1,
        ):

            if index > self.limits.max_steps:
                state.failure_reason = (
                    "step_limit_exceeded"
                )
                return state

            tool = self.tools.get(
                "enterprise_retrieval"
            )

            if tool is None:
                state.failure_reason = (
                    "retrieval_tool_unavailable"
                )
                return state

            evidence = tool.execute(
                sub_question,
                user,
            )

            evidence_sets.append(
                evidence
            )

            state.steps.append(
                AgentStep(
                    step_number=index,
                    question=sub_question,
                    tool=tool.name,
                    result_count=len(
                        evidence
                    ),
                    status="success",
                )
            )

        state.evidence = (
            self.evidence_aggregator.aggregate(
                evidence_sets
            )
        )

        if len(state.evidence) > (
            self.limits.max_evidence_documents
        ):
            state.evidence = state.evidence[
                : self.limits.max_evidence_documents
            ]

        state.completed = True

        return state