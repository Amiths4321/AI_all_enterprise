from app.core.security import (
    AccessPolicy,
    UserContext,
)
from app.services.secure_rag_service import (
    SecureRAGService,
)


class FakeRetrievalService:

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
                    "document": "HR policy",
                    "metadata": {
                        "department": "HR",
                        "access_level": "employee",
                        "allowed_roles": [
                            "employee",
                            "manager",
                        ],
                    },
                }
            ]
        }


class FakeGenerator:

    def generate(
        self,
        question,
        documents,
    ):
        assert all(
            document["metadata"]["department"]
            == "HR"
            for document in documents
        )

        return "Authorized answer"


def test_authorized_document_reaches_generator():

    service = SecureRAGService(
        retrieval_service=FakeRetrievalService(),
        generator=FakeGenerator(),
        access_policy=AccessPolicy(),
    )

    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    result = service.answer(
        "What is the HR policy?",
        user,
    )

    assert result["answer"] == "Authorized answer"
    assert result["security"]["authorized"] is True

class FinanceRetrievalService:

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
                    "document": "Finance confidential data",
                    "metadata": {
                        "department": "Finance",
                        "access_level": "manager",
                        "allowed_roles": ["manager"],
                    },
                }
            ]
        }


def test_unauthorized_document_never_reaches_generator():

    class GeneratorThatMustNeverRun:

        def generate(self, question, documents):
            raise AssertionError(
                "Unauthorized document reached generator"
            )

    service = SecureRAGService(
        retrieval_service=FinanceRetrievalService(),
        generator=GeneratorThatMustNeverRun(),
        access_policy=AccessPolicy(),
    )

    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    result = service.answer(
        "What is the finance budget?",
        user,
    )

    assert result["security"]["authorized"] is False
    assert result["documents"] == []
    