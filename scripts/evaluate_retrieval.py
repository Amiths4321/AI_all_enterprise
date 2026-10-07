
import json

from src.rag.pipeline import ParentChildRAG
from src.rag.multivector_pipeline import MultiVectorRAG


def evaluate_parent_child(rag, question, expected):
    results = rag.retrieve(question, k=20)
    ranked = rag.score_parents(results)

    retrieved = [
        item["parent_id"]
        for item in ranked[:3]
    ]

    hit = bool(set(retrieved) & set(expected))

    return retrieved, hit


def evaluate_multivector(rag, question, expected):
    results = rag.retrieve(question, k=12)
    parents = rag.aggregate_parents(results)
    ranked = rag.rerank(
        question,
        parents,
        top_k=3,
    )

    retrieved = [
        item["parent_id"]
        for item in ranked
    ]

    hit = bool(set(retrieved) & set(expected))

    return retrieved, hit


def main():

    with open(
        "tests/multivector_questions.json",
        "r",
        encoding="utf-8",
    ) as f:
        questions = json.load(f)

    parent_child = ParentChildRAG()
    multivector = MultiVectorRAG()

    pc_hits = 0
    mv_hits = 0

    print("=" * 80)
    print("RETRIEVAL EVALUATION")
    print("=" * 80)

    for index, item in enumerate(
        questions,
        start=1,
    ):

        question = item["question"]
        expected = item["expected_parent_ids"]

        print(
            f"\n[{index}/{len(questions)}] "
            f"{question}"
        )

        pc_retrieved, pc_hit = evaluate_parent_child(
            parent_child,
            question,
            expected,
        )

        mv_retrieved, mv_hit = evaluate_multivector(
            multivector,
            question,
            expected,
        )

        pc_hits += pc_hit
        mv_hits += mv_hit

        print(
            f"Expected:     {expected}"
        )

        print(
            f"Parent-Child: {pc_retrieved} "
            f"{'PASS' if pc_hit else 'FAIL'}"
        )

        print(
            f"Multi-Vector: {mv_retrieved} "
            f"{'PASS' if mv_hit else 'FAIL'}"
        )

    total = len(questions)

    print("\n" + "=" * 80)

    print(
        f"Parent-Child Recall@3: "
        f"{pc_hits}/{total} = "
        f"{pc_hits / total:.1%}"
    )

    print(
        f"Multi-Vector Recall@3: "
        f"{mv_hits}/{total} = "
        f"{mv_hits / total:.1%}"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()
