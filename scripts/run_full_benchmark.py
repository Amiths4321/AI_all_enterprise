import subprocess

import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.retrieval.multivector.store import MultiVectorStore


EXPECTED_VECTORS = 2540
EXPECTED_PARENTS = 635


STEPS = [
    (
        "Benchmark dataset validation",
        "scripts/validate_benchmark_dataset.py",
    ),
    (
        "Retriever benchmark",
        "scripts/benchmark_retrievers.py",
    ),
    (
        "Citation evaluation",
        "scripts/evaluate_citations.py",
    ),
    (
        "Answer quality",
        "scripts/evaluate_answers.py",
    ),
    (
        "Abstention testing",
        "scripts/test_abstention.py",
    ),
    (
        "Query expansion comparison",
        "scripts/compare_query_expansion.py",
    ),
    (
        "Regression test",
        "scripts/regression_test.py",
    ),
    (
        "Benchmark report",
        "scripts/generate_benchmark_report.py",
    ),
    ]


def database_complete():
    store = MultiVectorStore()

    vector_count = store.vectorstore._collection.count()

    data = store.vectorstore.get(
        include=["metadatas"]
    )

    metadatas = data.get("metadatas") or []

    parents = {
        metadata.get("parent_id")
        for metadata in metadatas
        if metadata.get("parent_id")
    }

    print("=" * 80)
    print("DATABASE READINESS CHECK")
    print("=" * 80)

    print(
        f"Vectors: {vector_count}/{EXPECTED_VECTORS}"
    )
    print(
        f"Parents: {len(parents)}/{EXPECTED_PARENTS}"
    )

    if vector_count != EXPECTED_VECTORS:
        return False

    if len(parents) != EXPECTED_PARENTS:
        return False

    return True


def run_step(name, script):
    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    start = time.perf_counter()

    result = subprocess.run(
        [sys.executable, script]
    )

    elapsed = time.perf_counter() - start

    print(
        f"\n{name} finished in "
        f"{elapsed:.2f}s"
    )

    if result.returncode != 0:
        print(
            f"\nFAILED: {script}"
        )
        return False

    return True


def main():
    print("=" * 80)
    print("ENTERPRISE RAG FULL BENCHMARK")
    print("=" * 80)

    if not database_complete():
        print("\nBenchmark NOT started.")
        print(
            "\nMulti-Vector ingestion is still incomplete."
        )
        print(
            f"Required: {EXPECTED_VECTORS} vectors / "
            f"{EXPECTED_PARENTS} parents"
        )
        return

    for name, script in STEPS:
        success = run_step(name, script)

        if not success:
            print(
                "\nBenchmark stopped after failure."
            )
            sys.exit(1)

    print("\n" + "=" * 80)
    print("ALL BENCHMARKS COMPLETED")
    print("=" * 80)

    print(
        "\nView the final retrieval comparison with:"
    )
    print(
        "python scripts\\show_benchmark.py"
    )


if __name__ == "__main__":
    main()