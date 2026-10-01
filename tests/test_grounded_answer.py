from app.core.security import (
    AccessPolicy,
    UserContext,
)

from app.services.grounded_answer import (
    GroundedAnswerService,
)


class FakeRetrieval:

    def retrieve(
        self,
        question,
        user,
        top_k=10,
        top_n=3,
    ):
        return {
            "reranked": [
                {
                    "id": "hr-001",
                    "document": (
                        "Employees receive "
                        "20 days of annual leave."
                    ),
                    "metadata": {
                        "department": "HR",
                        "access_level": "employee",
                        "allowed_roles": [
                            "employee",
                            "manager",
                        ],
                        "source": "hr_policy.txt",
                    },
                }
            ]
        }


class FakeGroundedGenerator:

    def generate(
        self,
        question,
        documents,
    ):

        return {
            "answer": (
                "Employees receive 20 days "
                "of annual leave [1]."
            ),
            "context_documents": [
                type(
                    "ContextDocument",
                    (),
                    {
                        "number": 1,
                        "document_id": "hr-001",
                        "source": "hr_policy.txt",
                    },
                )()
            ],
        }


def test_grounded_answer():

    service = GroundedAnswerService(
        retrieval_service=FakeRetrieval(),
        grounded_generator=FakeGroundedGenerator(),
        access_policy=AccessPolicy(),
    )

    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    result = service.answer(
        "How many leave days do employees receive?",
        user,
    )

    assert result["grounded"] is True
    assert result["citations"] == [
        {
            "number": 1,
            "document_id": "hr-001",
            "source": "hr_policy.txt",
        }
    ]

class HallucinatingGenerator:

    def generate(
        self,
        question,
        documents,
    ):

        return {
            "answer": (
                "Employees receive 20 days "
                "of annual leave [1]. "
                "Employees also receive unlimited "
                "personal leave."
            ),
            "context_documents": [
                type(
                    "ContextDocument",
                    (),
                    {
                        "number": 1,
                        "document_id": "hr-001",
                        "source": "hr_policy.txt",
                    },
                )()
            ],
        }


def test_hallucinated_claim_is_rejected():

    service = GroundedAnswerService(
        retrieval_service=FakeRetrieval(),
        grounded_generator=HallucinatingGenerator(),
        access_policy=AccessPolicy(),
    )

    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    result = service.answer(
        "How much leave do employees receive?",
        user,
    )

    assert result["grounded"] is False
    assert result["citations"] == []

class InvalidCitationGenerator:

    def generate(
        self,
        question,
        documents,
    ):

        return {
            "answer": (
                "Employees receive 20 days "
                "of annual leave [99]."
            ),
            "context_documents": [
                type(
                    "ContextDocument",
                    (),
                    {
                        "number": 1,
                        "document_id": "hr-001",
                        "source": "hr_policy.txt",
                    },
                )()
            ],
        }


def test_invalid_citation_is_rejected():

    service = GroundedAnswerService(
        retrieval_service=FakeRetrieval(),
        grounded_generator=InvalidCitationGenerator(),
        access_policy=AccessPolicy(),
    )

    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    result = service.answer(
        "How many leave days?",
        user,
    )

    assert result["grounded"] is False
    assert result["reason"] == "invalid_citation"

class UnauthorizedRetrieval:

    def retrieve(
        self,
        question,
        user,
        top_k=10,
        top_n=3,
    ):
        return {
            "reranked": [
                {
                    "id": "finance-001",
                    "document": (
                        "Confidential finance information."
                    ),
                    "metadata": {
                        "department": "Finance",
                        "access_level": "manager",
                        "allowed_roles": ["manager"],
                        "source": "finance_policy.txt",
                    },
                }
            ]
        }


class GeneratorMustNotReceiveUnauthorizedData:

    def generate(
        self,
        question,
        documents,
    ):
        raise AssertionError(
            "Security boundary failed"
        )


def test_unauthorized_information_cannot_reach_generation():

    service = GroundedAnswerService(
        retrieval_service=UnauthorizedRetrieval(),
        grounded_generator=(
            GeneratorMustNotReceiveUnauthorizedData()
        ),
        access_policy=AccessPolicy(),
    )

    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    result = service.answer(
        "What is the finance policy?",
        user,
    )

    assert result["grounded"] is False
    assert result["reason"] == "no_authorized_evidence"