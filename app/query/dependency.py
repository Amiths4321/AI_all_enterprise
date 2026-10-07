from dataclasses import dataclass


@dataclass(frozen=True)
class QueryNode:
    query_id: str
    question: str
    depends_on: list[str]