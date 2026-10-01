from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationCase:
    id: str
    question: str
    expected_document_ids: list[str]
    reference_answer: str

import json


def load_evaluation_cases(
    path: str,
) -> list[EvaluationCase]:

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        raw = json.load(file)

    return [
        EvaluationCase(
            id=item["id"],
            question=item["question"],
            expected_document_ids=item[
                "expected_document_ids"
            ],
            reference_answer=item[
                "reference_answer"
            ],
        )
        for item in raw
    ]

