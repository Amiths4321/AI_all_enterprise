import json
import statistics
from pathlib import Path


RESULTS_PATH = Path("tests/benchmark_results.json")
REPORT_PATH = Path("tests/benchmark_report.md")


LABELS = {
    "parent_child": "Parent-Child",
    "multivector": "Multi-Vector",
    "multivector_expanded": "Multi-Vector + Query Expansion",
}


def pct(value):
    return f"{value * 100:.1f}%"


def main():
    if not RESULTS_PATH.exists():
        print("Benchmark results not found.")
        print(
            "Run scripts\\benchmark_retrievers.py first."
        )
        return

    with RESULTS_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        results = json.load(f)

    question_count = results.get(
        "question_count",
        0,
    )

    if not question_count:
        print("Benchmark results are empty.")
        return

    lines = []

    lines.append("# Enterprise RAG Benchmark Report")
    lines.append("")
    lines.append(
        f"Questions evaluated: **{question_count}**"
    )
    lines.append("")

    lines.append("## Overall Results")
    lines.append("")
    lines.append(
        "| Retrieval Mode | Recall@1 | Recall@3 | MRR | Avg Latency |"
    )
    lines.append(
        "|---|---:|---:|---:|---:|"
    )

    for key, label in LABELS.items():
        section = results.get(key, {})
        summary = section.get("summary", {})

        if not summary:
            continue

        lines.append(
            f"| {label} "
            f"| {pct(summary.get('recall_at_1', 0))} "
            f"| {pct(summary.get('recall_at_3', 0))} "
            f"| {summary.get('mrr', 0):.3f} "
            f"| {summary.get('average_latency_seconds', 0):.3f}s |"
        )

    lines.append("")

    # Determine best retrieval mode.
    available = {}

    for key in LABELS:
        summary = results.get(key, {}).get(
            "summary"
        )

        if summary:
            available[key] = summary

    if available:
        best_r3 = max(
            available.items(),
            key=lambda item: item[1].get(
                "recall_at_3",
                0,
            ),
        )

        best_mrr = max(
            available.items(),
            key=lambda item: item[1].get(
                "mrr",
                0,
            ),
        )

        fastest = min(
            available.items(),
            key=lambda item: item[1].get(
                "average_latency_seconds",
                float("inf"),
            ),
        )

        lines.append("## Findings")
        lines.append("")

        lines.append(
            f"- Best Recall@3: "
            f"**{LABELS[best_r3[0]]}** "
            f"({pct(best_r3[1]['recall_at_3'])})"
        )

        lines.append(
            f"- Best MRR: "
            f"**{LABELS[best_mrr[0]]}** "
            f"({best_mrr[1]['mrr']:.3f})"
        )

        lines.append(
            f"- Lowest average latency: "
            f"**{LABELS[fastest[0]]}** "
            f"({fastest[1]['average_latency_seconds']:.3f}s)"
        )

        lines.append("")

    lines.append("## Per-Question Results")
    lines.append("")

    # Use the first populated section as the question list.
    first_section = next(
        (
            results[key]
            for key in LABELS
            if results.get(key, {}).get("questions")
        ),
        None,
    )

    if first_section:
        lines.append(
            "| Question | Mode | R@1 | R@3 | MRR | Latency |"
        )
        lines.append(
            "|---|---|---:|---:|---:|---:|"
        )

        for key, label in LABELS.items():
            section = results.get(key, {})
            questions = section.get(
                "questions",
                [],
            )

            for row in questions:
                lines.append(
                    f"| {row['question']} "
                    f"| {label} "
                    f"| {row['recall_at_1']:.2f} "
                    f"| {row['recall_at_3']:.2f} "
                    f"| {row['mrr']:.2f} "
                    f"| {row['latency_seconds']:.3f}s |"
                )

    lines.append("")
    lines.append("## Engineering Decision")
    lines.append("")
    lines.append(
        "The production retrieval strategy should be selected "
        "using retrieval quality together with latency and "
        "system complexity. Higher retrieval scores alone "
        "do not automatically justify a more expensive pipeline."
    )
    lines.append("")

    with REPORT_PATH.open(
        "w",
        encoding="utf-8",
    ) as f:
        f.write("\n".join(lines))

    print(
        f"Report written to: {REPORT_PATH}"
    )


if __name__ == "__main__":
    main()