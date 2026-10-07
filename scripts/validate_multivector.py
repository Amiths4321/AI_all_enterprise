import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


from collections import Counter

from src.retrieval.multivector.store import MultiVectorStore


EXPECTED_PARENTS = 635
EXPECTED_PER_PARENT = 4


def main():
    store = MultiVectorStore()

    data = store.vectorstore.get(
        include=["metadatas"]
    )

    metadatas = data.get("metadatas") or []

    counts = Counter(
        metadata.get("parent_id")
        for metadata in metadatas
        if metadata.get("parent_id")
    )

    print("=" * 80)
    print("MULTI-VECTOR INTEGRITY CHECK")
    print("=" * 80)

    print(f"Parents found: {len(counts)}")
    print(f"Vectors found: {len(metadatas)}")

    incomplete = [
        parent_id
        for parent_id, count in counts.items()
        if count != EXPECTED_PER_PARENT
    ]

    if not incomplete:
        print("\nEvery represented parent has exactly 4 vectors.")
    else:
        print(
            f"\nParents with incorrect vector counts: "
            f"{len(incomplete)}"
        )

        for parent_id in incomplete[:20]:
            print(
                f"  {parent_id}: "
                f"{counts[parent_id]} vectors"
            )

    print("\nRepresentation counts:")

    representation_counts = Counter(
        metadata.get("representation")
        for metadata in metadatas
    )

    for representation, count in representation_counts.items():
        print(f"  {representation}: {count}")

    print("=" * 80)


if __name__ == "__main__":
    main()