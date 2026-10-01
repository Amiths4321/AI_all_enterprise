from statistics import mean

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

from app.evaluation.dataset import (
    load_evaluation_cases,
)
from app.evaluation.retrieval_metrics import (
    recall_at_k,
    precision_at_k,
    reciprocal_rank,
    ndcg_at_k,
)


def main():

    cases = load_evaluation_cases(
        "data/evaluation_golden.json"
    )

    repository = ChromaDocumentRepository(
        path="chroma_db",
        collection_name="enterprise_documents",
    )

    vector_searcher = ChromaVectorSearcher(
        repository
    )

    documents = repository.get_all()

    retriever = HybridRetriever(
        documents,
        vector_searcher,
    )

    reranker = CrossEncoderReranker(
        model_name=(
            "cross-encoder/"
            "ms-marco-MiniLM-L-6-v2"
        )
    )

    results = []

    print()
    print("=" * 70)
    print("ENTERPRISE RAG RETRIEVAL EVALUATION")
    print("=" * 70)

    for case in cases:

        retrieved = retriever.retrieve(
            case.question,
            top_k=10,
            filters={},
            strategy="hybrid",
        )

        reranked = reranker.rerank(
            case.question,
            retrieved,
            top_n=3,
        )

        retrieved_ids = [
            document["id"]
            for document in reranked
        ]

        recall = recall_at_k(
            retrieved_ids,
            case.expected_document_ids,
            3,
        )

        precision = precision_at_k(
            retrieved_ids,
            case.expected_document_ids,
            3,
        )

        mrr = reciprocal_rank(
            retrieved_ids,
            case.expected_document_ids,
        )

        ndcg = ndcg_at_k(
            retrieved_ids,
            case.expected_document_ids,
            3,
        )

        results.append(
            {
                "recall": recall,
                "precision": precision,
                "mrr": mrr,
                "ndcg": ndcg,
            }
        )

        print()
        print(f"Case: {case.id}")
        print(f"Question: {case.question}")
        print(
            f"Expected: "
            f"{case.expected_document_ids}"
        )
        print(
            f"Retrieved: "
            f"{retrieved_ids}"
        )
        print(
            f"Recall@3:     {recall:.3f}"
        )
        print(
            f"Precision@3:  {precision:.3f}"
        )
        print(
            f"MRR:          {mrr:.3f}"
        )
        print(
            f"NDCG@3:       {ndcg:.3f}"
        )

    print()
    print("=" * 70)
    print("AGGREGATE RESULTS")
    print("=" * 70)

    if results:

        print(
            f"Recall@3:     "
            f"{mean(r['recall'] for r in results):.3f}"
        )

        print(
            f"Precision@3:  "
            f"{mean(r['precision'] for r in results):.3f}"
        )

        print(
            f"MRR:          "
            f"{mean(r['mrr'] for r in results):.3f}"
        )

        print(
            f"NDCG@3:       "
            f"{mean(r['ndcg'] for r in results):.3f}"
        )

    print()


if __name__ == "__main__":
    main()