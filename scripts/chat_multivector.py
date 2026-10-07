from src.rag.multivector_pipeline import (
    MultiVectorRAG,
)


def main():

    rag = MultiVectorRAG()

    print("=" * 80)
    print("MULTI-VECTOR RAG")
    print("=" * 80)

    while True:

        query = input(
            "\nQuestion (or 'exit'): "
        ).strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        result = rag.ask(query)

        print("\n" + "=" * 80)
        print("ANSWER")
        print("=" * 80)

        print(
            result["answer"]
        )

        print("\n" + "=" * 80)
        print("SOURCES")
        print("=" * 80)

        for source in result["sources"]:

            print(
                f"\n{source['parent_id']}"
            )

            print(
                f"Distance: "
                f"{source['distance']:.4f}"
            )

            print(
                f"Reranker: "
                f"{source['reranker_score']:.4f}"
            )

            print(
                "\nMatched question:"
            )

            print(
                source["representation"]
            )


if __name__ == "__main__":
    main()