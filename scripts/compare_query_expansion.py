
import json

from src.rag.multivector_pipeline import MultiVectorRAG


def main():

    with open(
        "tests/multivector_questions.json",
        "r",
        encoding="utf-8",
    ) as f:
        dataset = json.load(f)

    rag = MultiVectorRAG()

    no_expansion_hits = 0
    expansion_hits = 0

    print("=" * 80)
    print("QUERY EXPANSION COMPARISON")
    print("=" * 80)

    for index, item in enumerate(
        dataset,
        start=1,
    ):

        question = item["question"]
        expected = set(
            item["expected_parent_ids"]
        )

        print(
            f"\n{index}. {question}"
        )

        # Without expansion
        raw = rag.retrieve(
            question,
            k=12,
            expand=False,
        )

        parents = rag.aggregate_parents(
            raw
        )

        no_expansion = rag.rerank(
            question,
            parents,
            top_k=3,
        )

        no_expansion_ids = [
            item["parent_id"]
            for item in no_expansion
        ]

        # With expansion
        raw = rag.retrieve(
            question,
            k=8,
            expand=True,
        )

        parents = rag.aggregate_parents(
            raw
        )

        expansion = rag.rerank(
            question,
            parents,
            top_k=3,
        )

        expansion_ids = [
            item["parent_id"]
            for item in expansion
        ]

        no_hit = bool(
            expected
            & set(no_expansion_ids)
        )

        expansion_hit = bool(
            expected
            & set(expansion_ids)
        )

        no_expansion_hits += no_hit
        expansion_hits += expansion_hit

        print(
            f"Expected:      "
            f"{sorted(expected)}"
        )

        print(
            f"No expansion:  "
            f"{no_expansion_ids} "
            f"{'PASS' if no_hit else 'FAIL'}"
        )

        print(
            f"Expansion:     "
            f"{expansion_ids} "
            f"{'PASS' if expansion_hit else 'FAIL'}"
        )

    total = len(dataset)

    print("\n" + "=" * 80)

    print(
        f"No expansion Recall@3: "
        f"{no_expansion_hits}/{total} = "
        f"{no_expansion_hits / total:.1%}"
    )

    print(
        f"Expansion Recall@3: "
        f"{expansion_hits}/{total} = "
        f"{expansion_hits / total:.1%}"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()
