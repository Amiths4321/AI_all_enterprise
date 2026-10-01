from statistics import mean
from time import perf_counter

from app.retrieval.chroma_repository import (
    ChromaDocumentRepository,
)
from app.retrieval.chroma_vector import (
    ChromaVectorSearcher,
)
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.reranker import (
    CrossEncoderReranker,
)


QUESTIONS = [
    "How many annual leave days do employees receive?",
    "How do employees submit annual leave requests?",
    "What is required for production deployments?",
    "Who reviews the annual operating budget?",
]


def main():

    repository = ChromaDocumentRepository(
        path="chroma_db",
        collection_name="enterprise_documents",
    )

    vector_searcher = ChromaVectorSearcher(
        repository
    )

    retriever = HybridRetriever(
        repository.get_all(),
        vector_searcher,
    )

    reranker = CrossEncoderReranker()

    for candidate_depth in [
        3,
        5,
        10,
    ]:

        timings = []

        for question in QUESTIONS:

            started = perf_counter()

            retrieved = retriever.retrieve(
                question,
                top_k=candidate_depth,
                filters={},
                strategy="hybrid",
            )

            reranker.rerank(
                question,
                retrieved,
                top_n=3,
            )

            elapsed = (
                perf_counter()
                - started
            ) * 1000

            timings.append(elapsed)

        print()
        print(
            f"Candidate depth: "
            f"{candidate_depth}"
        )

        print(
            f"Average latency: "
            f"{mean(timings):.2f} ms"
        )


if __name__ == "__main__":
    main()