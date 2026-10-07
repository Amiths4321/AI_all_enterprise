import json
import statistics
import time
from datetime import datetime
from src.retrieval.multivector.store import MultiVectorStore

from src.rag.pipeline import ParentChildRAG
from src.rag.multivector_pipeline import MultiVectorRAG


QUESTIONS_PATH = "tests/multivector_questions.json"

def get_database_metadata():
    store = MultiVectorStore()

    data = store.vectorstore.get(
        include=["metadatas"]
    )
    database_metadata = get_database_metadata()

    metadatas = data.get("metadatas") or []

    parents = {
        metadata.get("parent_id")
        for metadata in metadatas
        if metadata.get("parent_id")
    }

    representation_counts = {}

    for metadata in metadatas:
        representation = metadata.get(
            "representation",
            "unknown",
        )

        representation_counts[representation] = (
            representation_counts.get(
                representation,
                0,
            )
            + 1
        )

    return {
        "timestamp": datetime.now().isoformat(),
        "vector_count": len(metadatas),
        "parent_count": len(parents),
        "representation_counts": representation_counts,
    }

def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def reciprocal_rank(retrieved_ids, expected_ids):
    expected = set(expected_ids)

    for rank, parent_id in enumerate(retrieved_ids, start=1):
        if parent_id in expected:
            return 1.0 / rank

    return 0.0


def recall_at_k(retrieved_ids, expected_ids, k):
    expected = set(expected_ids)

    if not expected:
        return 0.0

    retrieved = set(retrieved_ids[:k])

    return len(retrieved & expected) / len(expected)


def evaluate_mode(name, questions, runner):
    rows = []

    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    for index, item in enumerate(questions, start=1):
        question = item["question"]
        expected = item["expected_parent_ids"]

        start = time.perf_counter()

        result = runner(question)

        elapsed = time.perf_counter() - start

        sources = result.get("sources", [])

        retrieved_ids = [
            source["parent_id"]
            for source in sources
        ]

        row = {
            "question": question,
            "expected_parent_ids": expected,
            "retrieved_parent_ids": retrieved_ids,
            "recall_at_1": recall_at_k(
                retrieved_ids,
                expected,
                1,
            ),
            "recall_at_3": recall_at_k(
                retrieved_ids,
                expected,
                3,
            ),
            "mrr": reciprocal_rank(
                retrieved_ids,
                expected,
            ),
            "latency_seconds": elapsed,
        }

        rows.append(row)

        print(
            f"[{index}/{len(questions)}] "
            f"R@1={row['recall_at_1']:.2f} "
            f"R@3={row['recall_at_3']:.2f} "
            f"MRR={row['mrr']:.2f} "
            f"time={elapsed:.2f}s"
        )

    return rows


def summarize(rows):
    return {
        "recall_at_1": statistics.mean(
            row["recall_at_1"] for row in rows
        ),
        "recall_at_3": statistics.mean(
            row["recall_at_3"] for row in rows
        ),
        "mrr": statistics.mean(
            row["mrr"] for row in rows
        ),
        "average_latency_seconds": statistics.mean(
            row["latency_seconds"] for row in rows
        ),
    }


def main():
    questions = load_questions()

    print("=" * 80)
    print("CONTROLLED RETRIEVER BENCHMARK")
    print("=" * 80)
    print(f"Questions: {len(questions)}")

    parent_child = ParentChildRAG()
    multivector = MultiVectorRAG()

    parent_child_rows = evaluate_mode(
        "PARENT-CHILD",
        questions,
        lambda q: parent_child.ask(q),
    )

    multivector_rows = evaluate_mode(
        "MULTI-VECTOR",
        questions,
        lambda q: multivector.ask(
            q,
            expand=False,
        ),
    )

    multivector_expanded_rows = evaluate_mode(
        "MULTI-VECTOR + QUERY EXPANSION",
        questions,
        lambda q: multivector.ask(
            q,
            expand=True,
        ),
    )

    results = {
        "benchmark_metadata": database_metadata,
        "question_count": len(questions),
        "parent_child": {
            "summary": summarize(parent_child_rows),
            "questions": parent_child_rows,
        },
        "multivector": {
            "summary": summarize(multivector_rows),
            "questions": multivector_rows,
        },
        "multivector_expanded": {
            "summary": summarize(
                multivector_expanded_rows
            ),
            "questions": multivector_expanded_rows,
        },
    }

    output_path = "tests/benchmark_results.json"

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    for name in [
        "parent_child",
        "multivector",
        "multivector_expanded",
    ]:
        summary = results[name]["summary"]

        print(f"\n{name}")
        print(
            f"  Recall@1: "
            f"{summary['recall_at_1']:.3f}"
        )
        print(
            f"  Recall@3: "
            f"{summary['recall_at_3']:.3f}"
        )
        print(
            f"  MRR:      "
            f"{summary['mrr']:.3f}"
        )
        print(
            f"  Latency:  "
            f"{summary['average_latency_seconds']:.3f}s"
        )

    print(
        f"\nDetailed results saved to "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()