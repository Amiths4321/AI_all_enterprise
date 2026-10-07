from pathlib import Path
import sys

# Adds the project root directory to Python's module path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Then your imports below:
from src.retrieval.multivector.store import MultiVectorStore  # (Update path as needed)

def main():

    store = MultiVectorStore()

    query = input(
        "\nQuestion: "
    ).strip()

    results = store.search(
        query,
        k=5,
    )

    print("\n" + "=" * 80)
    print("MULTI-VECTOR RESULTS")
    print("=" * 80)

    for rank, (doc, score) in enumerate(
        results,
        start=1,
    ):

        print(
            f"\nRank: {rank}"
        )

        print(
            f"Distance: {score}"
        )

        print(
            f"Parent: "
            f"{doc.metadata.get('parent_id')}"
        )

        print(
            "\nMatched representation:"
        )

        print(
            doc.page_content
        )

        parent_id = doc.metadata.get(
            "parent_id"
        )

        parent = store.get_parent(
            parent_id
        )

        if parent:

            print(
                "\nOriginal parent:"
            )

            print(
                parent["text"][:1000]
            )


if __name__ == "__main__":
    main()
