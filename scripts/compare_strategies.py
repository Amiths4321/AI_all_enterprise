from app.evaluation.retrieval_metrics import (
    recall_at_k,
    reciprocal_rank,
)
from app.retrieval.chroma_repository import (
    ChromaDocumentRepository,
)
from app.retrieval.chroma_vector import (
    ChromaVectorSearcher,
)
from app.retrieval.hybrid import HybridRetriever


def main():

    repository = ChromaDocumentRepository(
        path="chroma_db",
        collection_name="enterprise_documents",
    )

    documents = repository.get_all()

    vector_searcher = ChromaVectorSearcher(
        repository=repository,
    )

    retriever = HybridRetriever(
        documents=documents,
        vector_searcher=vector_searcher,
    )

    cases = [
        {
            "question": (
                "How many annual leave days "
                "do employees receive?"
            ),
            "expected": ["hr-001"],
        },
        {
            "question": (
                "How do employees submit "
                "annual leave requests?"
            ),
            "expected": ["hr-002"],
        },
        {
            "question": (
                "What is required for "
                "production deployments?"
            ),
            "expected": ["engineering-001"],
        },
    ]

    for strategy in [
        "keyword",
        "vector",
        "hybrid",
    ]:

        recalls = []
        mrrs = []

        for case in cases:

            results = retriever.retrieve(
                question=case["question"],
                top_k=5,
                strategy=strategy,
            )

            ids = [
                item["id"]
                for item in results
            ]

            recalls.append(
                recall_at_k(
                    ids,
                    case["expected"],
                    k=5,
                )
            )

            mrrs.append(
                reciprocal_rank(
                    ids,
                    case["expected"],
                )
            )

        print(
            f"{strategy}: "
            f"Recall@5="
            f"{sum(recalls) / len(recalls):.3f}, "
            f"MRR="
            f"{sum(mrrs) / len(mrrs):.3f}"
        )


if __name__ == "__main__":
    main()