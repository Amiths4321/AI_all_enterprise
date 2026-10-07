from app.core.security import AccessPolicy, UserContext
from app.generation.citations import CitationExtractor, CitationVerifier


def test_employee_context_has_required_identity():
    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    assert user.user_id
    assert user.role
    assert user.department


def test_finance_document_is_not_visible_to_hr_employee():
    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    document = {
        "id": "finance-001",
        "document": "Finance leadership reviews the budget.",
        "metadata": {
            "department": "Finance",
            "access_level": "manager",
            "allowed_roles": ["manager"],
        },
    }

    policy = AccessPolicy()

    assert policy.can_access(user, document) is False


def test_authorized_hr_document_is_visible():
    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    document = {
        "id": "hr-001",
        "document": "Employees receive 20 days of annual leave.",
        "metadata": {
            "department": "HR",
            "access_level": "employee",
            "allowed_roles": ["employee", "manager"],
        },
    }

    policy = AccessPolicy()

    assert policy.can_access(user, document) is True


def test_citation_contract():
    answer = "Employees receive 20 days of annual leave [1]."

    documents = [
        {
            "id": "hr-001",
            "document": "Employees receive 20 days of annual leave.",
            "metadata": {},
        }
    ]

    extractor = CitationExtractor()
    verifier = CitationVerifier()

    citations = extractor.extract(answer)

    assert citations == [1]
    assert verifier.verify(citations, documents) is True