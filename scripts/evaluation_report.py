from statistics import mean


def summarize(results):

    if not results:
        return {}

    return {
        "cases": len(results),

        "recall_at_3": mean(
            result.recall_at_3
            for result in results
        ),

        "precision_at_3": mean(
            result.precision_at_3
            for result in results
        ),

        "mrr": mean(
            result.mrr
            for result in results
        ),

        "ndcg_at_3": mean(
            result.ndcg_at_3
            for result in results
        ),

        "answer_similarity": mean(
            result.answer_similarity
            for result in results
        ),

        "citation_precision": mean(
            result.citation_precision
            for result in results
        ),

        "citation_recall": mean(
            result.citation_recall
            for result in results
        ),

        "security_failures": sum(
            1
            for result in results
            if not result.security_passed
        ),
    }


def print_report(summary):

    print()
    print("=" * 60)
    print("ENTERPRISE RAG EVALUATION REPORT")
    print("=" * 60)

    for name, value in summary.items():

        if isinstance(value, float):
            print(
                f"{name:25} {value:.3f}"
            )
        else:
            print(
                f"{name:25} {value}"
            )