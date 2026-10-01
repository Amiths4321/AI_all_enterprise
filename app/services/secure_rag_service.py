from app.core.security import UserContext


class SecureRAGService:

    def __init__(
        self,
        retrieval_service,
        generator,
        access_policy,
    ):
        self.retrieval_service = retrieval_service
        self.generator = generator
        self.access_policy = access_policy

    def answer(
        self,
        question: str,
        user: UserContext,
        top_k: int = 10,
        top_n: int = 3,
    ):

        result = self.retrieval_service.retrieve(
            question=question,
            user=user,
            top_k=top_k,
            top_n=top_n,
        )

        documents = result["reranked"]

        authorized_documents = [
            document
            for document in documents
            if self.access_policy.can_access(
                user,
                document,
            )
        ]

        if not authorized_documents:
            return {
                "answer": "I don't have access to information needed to answer that question.",
                "documents": [],
                "citations": [],
                "security": {
                    "authorized": False,
                },
            }

        answer = self.generator.generate(
            question,
            authorized_documents,
        )

        citations = [
            {
                "id": document["id"],
                "source": document.get(
                    "metadata",
                    {},
                ).get("source"),
            }
            for document in authorized_documents
        ]

        return {
            "answer": answer,
            "documents": authorized_documents,
            "citations": citations,
            "security": {
                "authorized": True,
            },
        }