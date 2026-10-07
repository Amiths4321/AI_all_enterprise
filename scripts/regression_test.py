import json
import sys

from src.rag.multivector_pipeline import MultiVectorRAG


QUESTIONS_PATH = "tests/answer_questions.json"

MIN_CITATION_RATE = 0.80


def main():
    with open(
        QUESTIONS_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        questions = json.load(f)

    rag = MultiVectorRAG()

    passed = 0
    citation_ok = 0

    print("=" * 80)
    print("MULTI-VECTOR REGRESSION TEST")
    print("=" * 80)

    for index, item in enumerate(questions, start=1):
        question = item["question"]

        result = rag.ask(
            question,
            expand=False,
        )

        answer = result["answer"]
        sources = result.get("sources", [])

        has_citation = "[Source " in answer

        if answer.strip():
            passed += 1

        if has_citation:
            citation_ok += 1

        print(
            f"\n[{index}/{len(questions)}] "
            f"{question}"
        )

        print(
            f"  Answer generated: "
            f"{bool(answer.strip())}"
        )

        print(
            f"  Sources: "
            f"{len(sources)}"
        )

        print(
            f"  Citation present: "
            f"{has_citation}"
        )

    total = len(questions)

    answer_rate = (
        passed / total
        if total
        else 0
    )

    citation_rate = (
        citation_ok / total
        if total
        else 0
    )

    print("\n" + "=" * 80)
    print("REGRESSION SUMMARY")
    print("=" * 80)

    print(
        f"Answer generation: "
        f"{passed}/{total} "
        f"({answer_rate:.1%})"
    )

    print(
        f"Citation presence: "
        f"{citation_ok}/{total} "
        f"({citation_rate:.1%})"
    )

    success = (
        answer_rate == 1.0
        and citation_rate >= MIN_CITATION_RATE
    )

    print(
        f"\nRegression status: "
        f"{'PASS' if success else 'FAIL'}"
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()