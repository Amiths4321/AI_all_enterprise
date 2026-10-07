from typing import Any

from app.retrieval.hyde.generator import (
    HypotheticalDocumentGenerator,
)
from app.retrieval.hyde.generator import (
    HypotheticalDocumentGenerator,
)
from app.retrieval.hyde.result import (
    HyDERetrievalResult,
)


class HyDERetriever:

    def __init__(
        self,
        generator: HypotheticalDocumentGenerator,
        vector_searcher,
    ):
        self.generator = generator
        self.vector_searcher = vector_searcher

    def retrieve(
        self,
        question: str,
        top_k: int = 10,
        filters: dict | None = None,
    ) -> HyDERetrievalResult:

        hypothetical_document = (
            self.generator.generate(question)
        )

        documents = self.vector_searcher.search(
            hypothetical_document,
            top_k=top_k,
            filters=filters or {},
        )

        return HyDERetrievalResult(
            question=question,
            hypothetical_document=hypothetical_document,
            documents=documents,
        )
        def test_hyde_keeps_hypothetical_text_separate():

          class FakeGenerator:

            def generate(self, question):
                    return "Hypothetical unsupported passage."

          class FakeVectorSearcher:

            def search(
                    self,
                    question,
                    top_k=10,
                    filters=None,
          ):
                return [
                    {
                              "id": "hr-001",
                              "document": (
                              "Employees receive 20 days "
                              "of annual leave."
                              ),
                    }
                    ]

          from app.retrieval.hyde.retriever import (
          HyDERetriever,
          )

          retriever = HyDERetriever(
          generator=FakeGenerator(),
          vector_searcher=FakeVectorSearcher(),
          )

          result = retriever.retrieve(
          "How many leave days?"
          )

          assert (
          result.hypothetical_document
          == "Hypothetical unsupported passage."
          )

          assert len(result.documents) == 1

          assert all(
          document["id"] == "hr-001"
          for document in result.documents
          )      
    def retrieve(
        self,
        question: str,
        top_k: int = 10,
        filters: dict | None = None,
    ) -> list[dict[str, Any]]:

        hypothetical_document = (
            self.generator.generate(question)
        )

        results = self.vector_searcher.search(
            hypothetical_document,
            top_k=top_k,
            filters=filters or {},
        )

        return [
            {
                **document,
                "hyde": True,
                "hyde_query": hypothetical_document,
            }
            for document in results
        ]