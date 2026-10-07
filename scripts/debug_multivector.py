import sys
from pathlib import Path

# Automatically adds enterprise_rag to Python's path
sys.path.append(str(Path(__file__).resolve().parent.parent))


import time

from src.rag.multivector_pipeline import MultiVectorRAG


def main():

    rag = MultiVectorRAG()

    query = input(
        "\nQuestion: "
    ).strip()

    start = time.perf_counter()

    results = rag.retrieve(
        query,
        k=12,
    )

    retrieval_time = (
        time.perf_counter() - start
    )

    start = time.perf_counter()

    parents = rag.aggregate_parents(
        results
    )

    aggregation_time = (
        time.perf_counter() - start
    )

    start = time.perf_counter()

    reranked = rag.rerank(
        query,
        parents,
        top_k=3,
    )

    rerank_time = (
        time.perf_counter() - start
    )

    print("\n" + "=" * 80)
    print("MULTI-VECTOR RETRIEVAL DIAGNOSTICS")
    print("=" * 80)

    print(
        f"\nQuery: {query}"
    )

    print(
        f"\nRaw representations: "
        f"{len(results)}"
    )

    print(
        f"Unique parents: "
        f"{len(parents)}"
    )

    print(
        f"Final reranked parents: "
        f"{len(reranked)}"
    )

    print("\nTiming:")

    print(
        f"  Retrieval:   "
        f"{retrieval_time:.3f}s"
    )

    print(
        f"  Aggregation: "
        f"{aggregation_time:.3f}s"
    )

    print(
        f"  Reranking:   "
        f"{rerank_time:.3f}s"
    )

    print("\nTop representations:")

    for rank, (doc, distance) in enumerate(
        results,
        start=1,
    ):

        print(
            f"\n{rank}. "
            f"distance={distance:.4f}"
        )

        print(
            f"   parent="
            f"{doc.metadata.get('parent_id')}"
        )

        print(
            f"   type="
            f"{doc.metadata.get('representation')}"
        )

        print(
            f"   text="
            f"{doc.page_content[:250]}"
        )

    print("\nTop parents:")

    for rank, item in enumerate(
        reranked,
        start=1,
    ):

        print(
            f"\n{rank}. "
            f"{item['parent_id']}"
        )

        print(
            f"   aggregation score="
            f"{item['score']:.4f}"
        )

        print(
            f"   reranker score="
            f"{item['reranker_score']:.4f}"
        )

        for match in item["matches"]:
            print(
                f"   {match['type']}: "
                f"{match['distance']:.4f}"
            )


if __name__ == "__main__":
    main()
