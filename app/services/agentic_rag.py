from typing import Any

from app.agent.executor import AgentExecutor
from app.core.security import UserContext
from app.services.grounded_answer import GroundedAnswerService


class AgenticRAGService:

    def __init__(
        self,
        executor: AgentExecutor,
        grounded_answer_service: GroundedAnswerService,
    ):
        self.executor = executor
        self.grounded_answer_service = grounded_answer_service

    def answer(
        self,
        question: str,
        user: UserContext,
    ) -> dict[str, Any]:

        state = self.executor.execute(
            question=question,
            user=user,
        )

        evidence = state.evidence

        if not evidence:
            return {
                "question": question,
                "answer": (
                    "I cannot answer this question from the "
                    "authorized evidence available to you."
                ),
                "citations": [],
                "grounded": False,
                "agent_state": state,
            }

        grounded = self.grounded_answer_service.answer(
            question=question,
            documents=evidence,
        )

        return {
            "question": question,
            "answer": grounded["answer"],
            "citations": grounded.get("citations", []),
            "grounded": grounded.get("grounded", False),
            "agent_state": state,
        }