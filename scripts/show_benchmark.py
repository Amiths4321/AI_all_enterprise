import json
import os


RESULTS_PATH = "tests/benchmark_results.json"


def main():
    if not os.path.exists(RESULTS_PATH):
        print(f"Benchmark results not found: {RESULTS_PATH}")
        print("Run the benchmark first.")
        return

    with open(
        RESULTS_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        results = json.load(f)

    print("=" * 90)
    print("ENTERPRISE RAG BENCHMARK")
    print("=" * 90)

    # Detect old placeholder format.
    if "question_count" not in results:
        print("\nBenchmark results are not populated yet.")
        print("\nCurrent file contains:")

        for key in results:
            print(f"  - {key}")

        print(
            "\nRun the actual benchmark first:"
        )
        print(
            "  python scripts\\benchmark_retrievers.py"
        )

        return

    print(
        f"\nQuestions evaluated: "
        f"{results['question_count']}"
    )

    print("\n" + "-" * 90)

    print(
        f"{'Mode':<30}"
        f"{'R@1':>10}"
        f"{'R@3':>10}"
        f"{'MRR':>10}"
        f"{'Latency':>15}"
    )

    print("-" * 90)

    labels = {
        "parent_child": "Parent-Child",
        "multivector": "Multi-Vector",
        "multivector_expanded": (
            "Multi-Vector + Expansion"
        ),
    }

    for key, label in labels.items():
        if key not in results:
            continue

        summary = results[key].get("summary")

        if not summary:
            print(f"{label:<30}No results")
            continue

        print(
            f"{label:<30}"
            f"{summary.get('recall_at_1', 0):>10.3f}"
            f"{summary.get('recall_at_3', 0):>10.3f}"
            f"{summary.get('mrr', 0):>10.3f}"
            f"{summary.get('average_latency_seconds', 0):>14.3f}s"
        )

    print("-" * 90)


if __name__ == "__main__":
    main()