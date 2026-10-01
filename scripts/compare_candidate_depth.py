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

    for depth in [3, 5, 10]:

        recalls = []
        mrrs = []

        for case in cases:

            results = retriever.retrieve(
                question=case["question"],
                top_k=depth,
                strategy="hybrid",
            )

            ids = [
                item["id"]
                for item in results
            ]

            recalls.append(
                recall_at_k(
                    ids,
                    case["expected"],
                    k=depth,
                )
            )

            mrrs.append(
                reciprocal_rank(
                    ids,
                    case["expected"],
                )
            )

        average_recall = (
            sum(recalls)
            / len(recalls)
        )

        average_mrr = (
            sum(mrrs)
            / len(mrrs)
        )

        print(
            f"top_k={depth} "
            f"Recall={average_recall:.3f} "
            f"MRR={average_mrr:.3f}"
        )


if __name__ == "__main__":
    main()