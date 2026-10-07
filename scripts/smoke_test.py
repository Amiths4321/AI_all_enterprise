from src.rag.unified_pipeline import UnifiedRAG


def main():
    print("=" * 80)
    print("ENTERPRISE RAG SMOKE TEST")
    print("=" * 80)

    rag = UnifiedRAG()

    question = "What is the main purpose of this document?"

    print(f"\nQuestion: {question}")

    result = rag.ask(
        question,
        mode="multivector",
        expand=False,
    )

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result.get("sources", []):
        print(
            f"  {source['parent_id']} "
            f"score={source.get('score', 0):.4f}"
        )

    print("\nStatus: PASS")


if __name__ == "__main__":
    main()