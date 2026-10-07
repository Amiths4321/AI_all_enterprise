
import json
import re

from src.rag.multivector_pipeline import MultiVectorRAG


SOURCE_PATTERN = re.compile(
    r"\[Source\s+(\d+)\]"
)


def citation_check(
    answer,
    source_count,
):
    citations = [
        int(value)
        for value in SOURCE_PATTERN.findall(
            answer
        )
    ]

    invalid = [
        value
        for value in citations
        if value < 1 or value > source_count
    ]

    return {
        "citations": citations,
        "invalid": invalid,
        "valid": not invalid,
        "has_citation": bool(citations),
    }


def main():

    with open(
        "tests/answer_questions.json",
        "r",
        encoding="utf-8",
    ) as f:
        dataset = json.load(f)

    rag = MultiVectorRAG()

    citation_count = 0
    valid_count = 0

    print("=" * 80)
    print("CITATION EVALUATION")
    print("=" * 80)

    for index, item in enumerate(
        dataset,
        start=1,
    ):

        question = item["question"]

        result = rag.ask(
            question,
            expand=False,
        )

        answer = result["answer"]
        sources = result["sources"]

        check = citation_check(
            answer,
            len(sources),
        )

        if check["has_citation"]:
            citation_count += 1

        if check["valid"]:
            valid_count += 1

        print(
            f"\n{index}. {question}"
        )

        print(
            f"Citations: "
            f"{check['citations']}"
        )

        print(
            f"Valid: "
            f"{check['valid']}"
        )

        print(
            f"Answer:\n{answer}"
        )

    total = len(dataset)

    print("\n" + "=" * 80)

    print(
        f"Answers with citations: "
        f"{citation_count}/{total} "
        f"({citation_count / total:.1%})"
    )

    print(
        f"Answers with valid citations: "
        f"{valid_count}/{total} "
        f"({valid_count / total:.1%})"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()
