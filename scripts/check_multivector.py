from collections import Counter
import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Your existing imports
from src.retrieval.multivector.store import MultiVectorStore


EXPECTED_PARENTS = 635
EXPECTED_VECTORS = 2540
EXPECTED_QUESTIONS = 1905
EXPECTED_SUMMARIES = 635


def main():
    store = MultiVectorStore()

    count = store.vectorstore._collection.count()

    data = store.vectorstore.get(
        include=["metadatas"]
    )

    metadatas = data.get("metadatas") or []

    types = Counter(
        metadata.get("representation")
        for metadata in metadatas
    )

    parents = {
        metadata.get("parent_id")
        for metadata in metadatas
        if metadata.get("parent_id")
    }

    parent_count = len(parents)

    print("=" * 70)
    print("MULTI-VECTOR DATABASE STATUS")
    print("=" * 70)

    print(
        f"Total vectors: "
        f"{count}/{EXPECTED_VECTORS}"
    )

    print(
        f"Unique parents represented: "
        f"{parent_count}/{EXPECTED_PARENTS}"
    )

    print("\nRepresentation types:")

    questions = types.get(
        "hypothetical_question",
        0,
    )

    summaries = types.get(
        "summary",
        0,
    )

    print(
        f"  hypothetical_question: "
        f"{questions}/{EXPECTED_QUESTIONS}"
    )

    print(
        f"  summary: "
        f"{summaries}/{EXPECTED_SUMMARIES}"
    )

    vector_progress = (
        count / EXPECTED_VECTORS
        if EXPECTED_VECTORS
        else 0
    )

    parent_progress = (
        parent_count / EXPECTED_PARENTS
        if EXPECTED_PARENTS
        else 0
    )

    print("\nProgress:")

    print(
        f"  Vectors: "
        f"{vector_progress:.1%}"
    )

    print(
        f"  Parents: "
        f"{parent_progress:.1%}"
    )

    complete = (
        count == EXPECTED_VECTORS
        and parent_count == EXPECTED_PARENTS
        and questions == EXPECTED_QUESTIONS
        and summaries == EXPECTED_SUMMARIES
    )

    print("\nBenchmark readiness:")

    if complete:
        print("  READY")
        print(
            "\nRun:"
        )
        print(
            "  python scripts\\run_full_benchmark.py"
        )
    else:
        print("  NOT READY")
        print(
            "\nKeep ingestion running."
        )

    print("=" * 70)


if __name__ == "__main__":
    main()