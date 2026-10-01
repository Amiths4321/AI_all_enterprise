from dataclasses import dataclass, field


@dataclass
class AgentStep:
    step_number: int
    question: str
    tool: str
    result_count: int
    status: str


@dataclass
class AgentState:
    original_question: str

    sub_questions: list[str] = field(
        default_factory=list
    )

    evidence: list[dict] = field(
        default_factory=list
    )

    steps: list[AgentStep] = field(
        default_factory=list
    )

    completed: bool = False
    failure_reason: str | None = None