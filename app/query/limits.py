from dataclasses import dataclass


@dataclass(frozen=True)
class QueryLimits:
    max_sub_questions: int = 5
    max_parallel_queries: int = 4