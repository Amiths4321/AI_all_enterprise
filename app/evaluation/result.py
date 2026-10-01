from dataclasses import dataclass


@dataclass
class EvaluationResult:

    case_id: str

    recall_at_3: float
    precision_at_3: float
    mrr: float
    ndcg_at_3: float

    answer_similarity: float

    citation_precision: float
    citation_recall: float
    citation_validity: float

    security_passed: bool
    security_leakage_count: int