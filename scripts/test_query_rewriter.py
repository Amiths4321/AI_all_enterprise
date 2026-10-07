
from src.rag.query_rewriter import QueryRewriter


def main():

    rewriter = QueryRewriter()

    history = [
        (
            "user",
            "What is the main purpose of this handbook?"
        ),
        (
            "assistant",
            "It provides construction detailing "
            "information for building professionals."
        ),
    ]

    query = "Who is it intended for?"

    result = rewriter.rewrite(
        query,
        history,
    )

    print("\nOriginal:")
    print(query)

    print("\nRewritten:")
    print(result)


if __name__ == "__main__":
    main()
