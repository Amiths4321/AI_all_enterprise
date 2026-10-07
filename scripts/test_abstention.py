import json
import re

from src.rag.multivector_pipeline import MultiVectorRAG


ABSTENTION_PATTERNS = [
    r"do not have enough information",
    r"not enough information",
    r"cannot answer",
    r"can't answer",
    r"not provided",
    r"not mentioned",
    r"not available",
    r"insufficient information",
]


def is_abstention(answer):
    text = answer.lower()

    return any(
        re.search(pattern, text)
        for pattern in ABSTENTION_PATTERNS
    )


def main():
    with open(
        "tests/abstention_questions.json",
        "r",
        encoding="utf-8",
    ) as f:
        questions = json.load(f)

    rag = MultiVectorRAG()

    passed = 0

    print("=" * 80)
    print("RAG ABSTENTION TEST")
    print("=" * 80)

    for index, item in enumerate(questions, start=1):
        question = item["question"]

        result = rag.ask(
            question,
            expand=False,
        )

        answer = result["answer"]

        success = is_abstention(answer)

        if success:
            passed += 1

        print(f"\n[{index}] {question}")
        print(f"PASS: {success}")
        print(f"Answer: {answer}")

    total = len(questions)
    accuracy = passed / total if total else 0

    print("\n" + "=" * 80)
    print(f"Abstention accuracy: {passed}/{total}")
    print(f"Rate: {accuracy:.1%}")
    print("=" * 80)


if __name__ == "__main__":
    main()