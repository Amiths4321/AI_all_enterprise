from app.generation.citations import (
    CitationExtractor,
    CitationVerifier,
)
from app.generation.grounding import (
    GroundingChecker,
)
from app.generation.evidence_gate import (
    EvidenceSufficiencyGate,
)
from app.generation.refusal import (
    RefusalGenerator,
)


class GroundedAnswerService:

    def __init__(
        self,
        retrieval_service,
        grounded_generator,
        access_policy,
    ):
        self.retrieval_service = retrieval_service
        self.grounded_generator = grounded_generator
        self.access_policy = access_policy

        self.evidence_gate = (
            EvidenceSufficiencyGate()
        )

        self.citation_verifier = (
            CitationVerifier()
        )

        self.grounding_checker = (
            GroundingChecker()
        )

        self.refusal = RefusalGenerator()

    def answer(
        self,
        question,
        user,
        top_k=10,
        top_n=3,
    ):

        retrieval = self.retrieval_service.retrieve(
            question=question,
            user=user,
            top_k=top_k,
            top_n=top_n,
        )

        documents = retrieval["reranked"]

        documents = [
            document
            for document in documents
            if self.access_policy.can_access(
                user,
                document,
            )
        ]

        evidence = self.evidence_gate.check(
            documents
        )

        if not evidence["sufficient"]:
            return {
                "answer": self.refusal.insufficient_evidence(),
                "citations": [],
                "grounded": False,
                "reason": evidence["reason"],
            }

        generated = self.grounded_generator.generate(
            question,
            documents,
        )

        answer = generated["answer"]

        context_documents = generated[
            "context_documents"
        ]

        citation_result = (
            self.citation_verifier.verify(
                answer,
                context_documents,
            )
        )

        grounding_result = (
            self.grounding_checker.check(
                answer
            )
        )

        if not citation_result["valid"]:
            return {
                "answer": self.refusal.insufficient_evidence(),
                "citations": [],
                "grounded": False,
                "reason": "invalid_citation",
            }

        if not grounding_result["grounded"]:
            return {
                "answer": self.refusal.insufficient_evidence(),
                "citations": [],
                "grounded": False,
                "reason": "uncited_claim",
            }

        citations = []

        for number in citation_result["citations"]:

            document = next(
                (
                    document
                    for document in context_documents
                    if document.number == number
                ),
                None,
            )

            if document:
                citations.append(
                    {
                        "number": number,
                        "document_id": document.document_id,
                        "source": document.source,
                    }
                )

        return {
            "answer": answer,
            "citations": citations,
            "grounded": True,
            "reason": "grounded_answer",
        }