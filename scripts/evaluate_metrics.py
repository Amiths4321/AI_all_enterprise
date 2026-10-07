
import json
from datetime import datetime

from src.rag.pipeline import ParentChildRAG
from src.rag.multivector_pipeline import MultiVectorRAG


RESULT_PATH = "tests/retrieval_results.json"


def recall_at_k(retrieved, expected, k):
    return int(
        bool(
            set(retrieved[:k])
            & set(expected)
        )
    )


def reciprocal_rank(retrieved, expected):
    expected = set(expected)

    for rank, parent_id in enumerate(
        retrieved,
        start=1,
    ):
        if parent_id in expected:
            return 1.0 / rank

    return 0.0


def evaluate_parent_child(rag, question):
    results = rag.retrieve(
        question,
        k=20,
    )

    ranked = rag.score_parents(results)

    return [
        item["parent_id"]
        for item in ranked
    ]


def evaluate_multivector(rag, question):
    results = rag.retrieve(
        question,
        k=12,
    )

    parents = rag.aggregate_parents(
        results
    )

    ranked = rag.rerank(
        question,
        parents,
        top_k=10,
    )

    return [
        item["parent_id"]
        for item in ranked
    ]


def main():

    with open(
        "tests/multivector_questions.json",
        "r",
        encoding="utf-8",
    ) as f:
        dataset = json.load(f)

    parent_child = ParentChildRAG()
    multivector = MultiVectorRAG()

    pc_r1 = []
    pc_r3 = []
    pc_mrr = []

    mv_r1 = []
    mv_r3 = []
    mv_mrr = []

    details = []

    print("=" * 80)
    print("RETRIEVAL METRICS")
    print("=" * 80)

    for index, item in enumerate(
        dataset,
        start=1,
    ):

        question = item["question"]
        expected = item["expected_parent_ids"]

        pc = evaluate_parent_child(
            parent_child,
            question,
        )

        mv = evaluate_multivector(
            multivector,
            question,
        )

        pc1 = recall_at_k(
            pc,
            expected,
            1,
        )

        pc3 = recall_at_k(
            pc,
            expected,
            3,
        )

        pcmrr = reciprocal_rank(
            pc,
            expected,
        )

        mv1 = recall_at_k(
            mv,
            expected,
            1,
        )

        mv3 = recall_at_k(
            mv,
            expected,
            3,
        )

        mvmrr = reciprocal_rank(
            mv,
            expected,
        )

        pc_r1.append(pc1)
        pc_r3.append(pc3)
        pc_mrr.append(pcmrr)

        mv_r1.append(mv1)
        mv_r3.append(mv3)
        mv_mrr.append(mvmrr)

        details.append(
            {
                "question": question,
                "expected": expected,
                "parent_child": {
                    "retrieved": pc[:10],
                    "recall_at_1": pc1,
                    "recall_at_3": pc3,
                    "reciprocal_rank": pcmrr,
                },
                "multi_vector": {
                    "retrieved": mv[:10],
                    "recall_at_1": mv1,
                    "recall_at_3": mv3,
                    "reciprocal_rank": mvmrr,
                },
            }
        )

        print(
            f"\n{index}. {question}"
        )

        print(
            f"  PC: {pc[:5]}"
        )

        print(
            f"  MV: {mv[:5]}"
        )

    total = len(dataset)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "questions": total,
        "parent_child": {
            "recall_at_1": sum(pc_r1) / total,
            "recall_at_3": sum(pc_r3) / total,
            "mrr": sum(pc_mrr) / total,
        },
        "multi_vector": {
            "recall_at_1": sum(mv_r1) / total,
            "recall_at_3": sum(mv_r3) / total,
            "mrr": sum(mv_mrr) / total,
        },
        "details": details,
    }

    with open(
        RESULT_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            summary,
            f,
            indent=2,
        )

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(
        f"Parent-Child Recall@1: "
        f"{summary['parent_child']['recall_at_1']:.1%}"
    )

    print(
        f"Parent-Child Recall@3: "
        f"{summary['parent_child']['recall_at_3']:.1%}"
    )

    print(
        f"Parent-Child MRR: "
        f"{summary['parent_child']['mrr']:.3f}"
    )

    print()

    print(
        f"Multi-Vector Recall@1: "
        f"{summary['multi_vector']['recall_at_1']:.1%}"
    )

    print(
        f"Multi-Vector Recall@3: "
        f"{summary['multi_vector']['recall_at_3']:.1%}"
    )

    print(
        f"Multi-Vector MRR: "
        f"{summary['multi_vector']['mrr']:.3f}"
    )

    print(
        f"\nResults saved to: {RESULT_PATH}"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()
