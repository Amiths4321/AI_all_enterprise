from dataclasses import dataclass


@dataclass(frozen=True)
class AgentLimits:

    max_steps: int = 5
    max_sub_questions: int = 5
    max_evidence_documents: int = 20