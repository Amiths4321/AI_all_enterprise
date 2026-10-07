import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.rag.multivector_pipeline import (
    MultiVectorRAG,
)


def main():

    with open(
        "tests/multivector_questions.json",
        "r",
        encoding="utf-8",
    ) as f:

        questions = json.load(f)

    rag = MultiVectorRAG()

    correct = 0

    print("=" * 80)
    print("MULTI-VECTOR EVALUATION")
    print("=" * 80)

    for index, item in enumerate(
        questions,
        start=1,
    ):

        question = item["question"]

        expected = set(
            item["expected_parent_ids"]
        )

        results = rag.retrieve(
            question,
            k=10,
        )

        reranked = rag.rerank(
            question,
            results,
            top_k=3,
        )

        retrieved = set(
            result["parent_id"]
            for result in reranked
        )

        hit = bool(
            expected.intersection(
                retrieved
            )
        )

        if hit:
            correct += 1

        print(
            f"\n{index}. {question}"
        )

        print(
            f"Expected: {sorted(expected)}"
        )

        print(
            f"Retrieved: {sorted(retrieved)}"
        )

        print(
            "PASS"
            if hit
            else "FAIL"
        )

    recall = (
        correct / len(questions)
    )

    print("\n" + "=" * 80)

    print(
        f"Recall@3: "
        f"{correct}/{len(questions)} "
        f"= {recall:.1%}"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()