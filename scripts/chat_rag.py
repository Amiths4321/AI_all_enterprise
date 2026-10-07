from pathlib import Path
import sys

# Adds the project root to sys.path if running from scripts/
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.rag.pipeline import ParentChildRAG


def main():

    rag = ParentChildRAG()

    chat_history = []

    print("=" * 80)
    print("PARENT-CHILD RAG")
    print("=" * 80)

    while True:

        query = input("\nQuestion (or 'exit'): ").strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        result = rag.ask(
            query,
            chat_history,
        )

        print("\n" + "=" * 80)
        print("ANSWER")
        print("=" * 80)

        print(result["answer"])

        print("\n" + "=" * 80)
        print("SOURCES")
        print("=" * 80)

        # Use enumerate to safely track and print source ranking
        for rank, source in enumerate(result["sources"], start=1):

            print(
                f"\n[{rank}] "
                f"{source.get('parent_id', 'N/A')}"
            )

            print(
                f"Score: {source.get('score', 0.0):.4f}"
            )

            print(
                f"Children matched: "
                f"{source.get('children_hit', 'N/A')}"
            )

            print("\nSource text:")
            print(source.get("text", "")[:1000])

        chat_history.append(
            ("user", query)
        )

        chat_history.append(
            ("assistant", result["answer"])
        )


if __name__ == "__main__":
    main()