from dataclasses import dataclass, field


@dataclass(frozen=True)
class QueryIntent:
    intent: str
    confidence: float


@dataclass(frozen=True)
class QueryEntity:
    name: str
    entity_type: str


@dataclass
class QueryPlan:
    original_question: str
    normalized_question: str
    intents: list[QueryIntent] = field(default_factory=list)
    entities: list[QueryEntity] = field(default_factory=list)
    sub_questions: list[str] = field(default_factory=list)
    retrieval_queries: list[str] = field(default_factory=list)