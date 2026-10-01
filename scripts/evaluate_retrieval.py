import json
from pathlib import Path

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
from app.retrieval.reranker import (
    CrossEncoderReranker,
)


GOLDEN_FILE = Path("data/retrieval_golden.json")


def load_golden():
    with GOLDEN_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def evaluate_case(
    retrieved_ids,
    expected_ids,
):
    return {
        "recall_at_3": recall_at_k(
            retrieved_ids,
            expected_ids,
            k=3,
        ),
        "recall_at_5": recall_at_k(
            retrieved_ids,
            expected_ids,
            k=5,
        ),
        "mrr": reciprocal_rank(
            retrieved_ids,
            expected_ids,
        ),
    }


def main():

    golden = load_golden()

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

    reranker = CrossEncoderReranker()

    results = []

    for case in golden:

        retrieved = retriever.retrieve(
            question=case["question"],
            top_k=10,
            strategy="hybrid",
        )

        reranked = reranker.rerank(
            question=case["question"],
            documents=retrieved,
            top_n=5,
        )

        retrieved_ids = [
            item["id"]
            for item in reranked
        ]

        metrics = evaluate_case(
            retrieved_ids=retrieved_ids,
            expected_ids=case[
                "expected_document_ids"
            ],
        )

        results.append(
            {
                "question": case["question"],
                "retrieved_ids": retrieved_ids,
                "expected_ids": case[
                    "expected_document_ids"
                ],
                "metrics": metrics,
            }
        )

    aggregate_recall_3 = sum(
        item["metrics"]["recall_at_3"]
        for item in results
    ) / len(results)

    aggregate_mrr = sum(
        item["metrics"]["mrr"]
        for item in results
    ) / len(results)

    print("\nRETRIEVAL EVALUATION")
    print("====================")

    for item in results:

        print(
            f"\nQuestion: {item['question']}"
        )

        print(
            f"Expected: {item['expected_ids']}"
        )

        print(
            f"Retrieved: {item['retrieved_ids']}"
        )

        print(
            f"Recall@3: "
            f"{item['metrics']['recall_at_3']:.3f}"
        )

        print(
            f"MRR: "
            f"{item['metrics']['mrr']:.3f}"
        )

    print("\nAGGREGATE")

    print(
        f"Recall@3: {aggregate_recall_3:.3f}"
    )

    print(
        f"MRR: {aggregate_mrr:.3f}"
    )