from dataclasses import dataclass


@dataclass
class QueryAnalysis:
    original_question: str
    normalized_question: str
    department: str | None = None
    document_type: str | None = None
    year: int | None = None


class QueryAnalyzer:

    DEPARTMENTS = {
        "hr": "HR",
        "finance": "Finance",
        "engineering": "Engineering",
    }

    def analyze(self, question: str) -> QueryAnalysis:

        normalized = " ".join(
            question.strip().split()
        )

        lower = normalized.lower()

        department = None

        for keyword, value in self.DEPARTMENTS.items():
            if keyword in lower:
                department = value
                break

        document_type = None

        if "policy" in lower:
            document_type = "policy"
        elif (
            "procedure" in lower
            or "process" in lower
        ):
            document_type = "procedure"

        year = None

        for candidate in range(2020, 2031):
            if str(candidate) in lower:
                year = candidate
                break

        return QueryAnalysis(
            original_question=question,
            normalized_question=normalized,
            department=department,
            document_type=document_type,
            year=year,
        )