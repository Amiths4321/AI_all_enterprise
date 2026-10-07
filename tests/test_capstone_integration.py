from app.core.security import UserContext


def test_hr_employee_can_access_hr_documents():
    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    assert user.department == "HR"
    assert user.role == "employee"

from app.core.security import AccessPolicy


def test_hr_employee_cannot_access_finance_document():

    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    finance_document = {
        "id": "finance-001",
        "document": (
            "The annual operating budget is reviewed "
            "by the finance leadership team."
        ),
        "metadata": {
            "department": "Finance",
            "access_level": "manager",
            "allowed_roles": ["manager"],
        },
    }

    policy = AccessPolicy()

    assert policy.can_access(
        user,
        finance_document,
    ) is False

from app.generation.citations import (
    CitationExtractor,
    CitationVerifier,
)


def test_valid_citation_is_accepted():

    answer = (
        "Employees receive 20 days of annual leave "
        "[1]."
    )

    documents = [
        {
            "id": "hr-001",
            "document": (
                "Employees receive 20 days of annual "
                "leave per calendar year."
            ),
            "metadata": {
                "source": "hr_policy.txt"
            },
        }
    ]

    extractor = CitationExtractor()
    verifier = CitationVerifier()

    citations = extractor.extract(answer)

    assert citations == [1]

    assert verifier.verify(
        citations,
        documents,
    ) is True

def test_invalid_citation_is_rejected():

    answer = (
        "Employees receive 20 days of annual leave [7]."
    )

    documents = [
        {
            "id": "hr-001",
            "document": (
                "Employees receive 20 days of annual "
                "leave per calendar year."
            ),
            "metadata": {
                "source": "hr_policy.txt"
            },
        }
    ]

    extractor = CitationExtractor()
    verifier = CitationVerifier()

    citations = extractor.extract(answer)

    assert verifier.verify(
        citations,
        documents,
    ) is False