import sys
from pathlib import Path

# Adds the parent directory (enterprise_rag) to Python's path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.rag.unified_pipeline import UnifiedRAG


def print_sources(sources):

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for index, source in enumerate(
        sources,
        start=1,
    ):

        print(
            f"\n[{index}] "
            f"{source['parent_id']}"
        )

        print(
            f"Retrieval score: "
            f"{source.get('score', 0):.4f}"
        )

        print(
            f"Reranker score: "
            f"{source.get('reranker_score', 0):.4f}"
        )

        print(
            source["text"][:500]
        )


def main():

    rag = UnifiedRAG()

    print("=" * 80)
    print("ENTERPRISE RAG")
    print("=" * 80)

    print(
        "\nModes:"
        "\n  1 = Parent-Child"
        "\n  2 = Multi-Vector"
        "\n  3 = Multi-Vector + Query Expansion"
        "\n  q = Quit"
    )

    while True:

        mode = input(
            "\nMode: "
        ).strip().lower()

        if mode == "q":
            break

        if mode == "1":
            retrieval_mode = "parent_child"
            expand = False

        elif mode == "2":
            retrieval_mode = "multivector"
            expand = False

        elif mode == "3":
            retrieval_mode = "multivector"
            expand = True

        else:
            print("Invalid mode.")
            continue

        question = input(
            "Question: "
        ).strip()

        if not question:
            continue

        print("\nThinking...\n")

        try:

            result = rag.ask(
                question,
                mode=retrieval_mode,
                expand=expand,
            )

            print("=" * 80)
            print("ANSWER")
            print("=" * 80)

            print(
                f"\n{result['answer']}"
            )

            print_sources(
                result["sources"]
            )

        except Exception as exc:

            print(
                f"\nERROR: {exc}"
            )


if __name__ == "__main__":
    main()
