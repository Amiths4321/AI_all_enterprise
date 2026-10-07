import json

from src.retrieval.multivector.store import MultiVectorStore


QUESTIONS_PATH = "tests/multivector_questions.json"


def main():
    
    with open(
        QUESTIONS_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        questions = json.load(f)

    store = MultiVectorStore()

    data = store.vectorstore.get(
        include=["metadatas"]
    )

    metadatas = data.get("metadatas") or []

    available_parents = {
        metadata.get("parent_id")
        for metadata in metadatas
        if metadata.get("parent_id")
    }

    print("=" * 80)
    print("BENCHMARK DATASET VALIDATION")
    print("=" * 80)

    print(f"Questions: {len(questions)}")
    print(f"Available parents: {len(available_parents)}")

    errors = []

    for index, item in enumerate(questions, start=1):
        question = item.get("question")
        expected = item.get("expected_parent_ids")

        if not question:
            errors.append(
                f"Question {index}: missing question"
            )

        if not expected:
            errors.append(
                f"Question {index}: missing expected parents"
            )
            continue

        unknown = [
            parent_id
            for parent_id in expected
            if parent_id not in available_parents
        ]

        if unknown:
            errors.append(
                f"Question {index}: unknown parents "
                f"{unknown}"
            )

    print("\nValidation:")

    if errors:
        print("FAILED")

        for error in errors:
            print(f"  - {error}")
    else:
        print("PASSED")
        print(
            "All expected parent IDs exist in the "
            "Multi-Vector database."
        )

    print("=" * 80)


if __name__ == "__main__":
    main()