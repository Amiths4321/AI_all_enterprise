import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rag.pipeline import ParentChildRAG
from src.rag.multivector_pipeline import MultiVectorRAG


def evaluate_parent_child(rag, question, expected):
    results = rag.retrieve(question, k=20)
    ranked = rag.score_parents(results)

    retrieved = [
        item["parent_id"]
        for item in ranked[:3]
    ]

    return retrieved, bool(set(retrieved) & set(expected))


def evaluate_multivector(rag, question, expected):
    results = rag.retrieve(question, k=10)
    ranked = rag.rerank(question, results, top_k=3)

    retrieved = [
        item["parent_id"]
        for item in ranked
    ]

    return retrieved, bool(set(retrieved) & set(expected))


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
    print("PARENT-CHILD VS MULTI-VECTOR")
    print("=" * 80)

    for i, item in enumerate(questions, start=1):
        question = item["question"]
        expected = item["expected_parent_ids"]

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

        print(f"\n{i}. {question}")
        print(f"Expected:       {expected}")
        print(f"Parent-Child:   {pc_retrieved} -> "
              f"{'PASS' if pc_hit else 'FAIL'}")
        print(f"Multi-Vector:   {mv_retrieved} -> "
              f"{'PASS' if mv_hit else 'FAIL'}")

    total = len(questions)

    print("\n" + "=" * 80)
    print(f"Parent-Child Recall@3: "
          f"{pc_hits}/{total} = {pc_hits / total:.1%}")

    print(f"Multi-Vector Recall@3: "
          f"{mv_hits}/{total} = {mv_hits / total:.1%}")

    print("=" * 80)


if __name__ == "__main__":
    main()