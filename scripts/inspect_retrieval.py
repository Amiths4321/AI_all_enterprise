
import sys
from pathlib import Path

# Adds the parent directory (enterprise_rag) to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.rag.multivector_pipeline import MultiVectorRAG


def main():
    rag = MultiVectorRAG()

    query = input("\nQuestion: ").strip()

    print("\n" + "=" * 80)
    print("RAW MULTI-VECTOR RESULTS")
    print("=" * 80)

    results = rag.retrieve(query, k=12, expand=False)

    for rank, result in enumerate(results, start=1):
        doc = result["doc"]
        distance = result["distance"]

        print(f"\n[{rank}] distance={distance:.4f}")
        print(f"parent_id: {doc.metadata.get('parent_id')}")
        print(f"type:      {doc.metadata.get('representation')}")
        print(
            f"match:     "
            f"{doc.page_content[:500].replace(chr(10), ' ')}"
        )

    print("\n" + "=" * 80)
    print("PARENT AGGREGATION")
    print("=" * 80)

    parents = rag.aggregate_parents(results)

    for rank, item in enumerate(parents[:10], start=1):
        print(f"\n[{rank}] parent={item['parent_id']}")
        print(f"score={item['score']:.4f}")

        for match in item["matches"]:
            print(
                f"  - {match['type']}: "
                f"{match['distance']:.4f} | "
                f"{match['representation'][:200].replace(chr(10), ' ')}"
            )

    print("\n" + "=" * 80)
    print("RERANKED RESULTS")
    print("=" * 80)

    reranked = rag.rerank(query, parents, top_k=5)

    for rank, item in enumerate(reranked, start=1):
        print(f"\n[{rank}] {item['parent_id']}")
        print(f"retrieval_score={item['score']:.4f}")
        print(f"reranker_score={item['reranker_score']:.4f}")
        print(f"text={item['text'][:700].replace(chr(10), ' ')}")


if __name__ == "__main__":
    main()