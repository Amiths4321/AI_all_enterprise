
import json

from src.rag.pipeline import ParentChildRAG
from src.rag.multivector_pipeline import MultiVectorRAG


def evaluate_answer(llm, question, reference, answer):
    prompt = f"""
Evaluate the following RAG answer.

Question:
{question}

Reference answer:
{reference}

Generated answer:
{answer}

Score the generated answer from 1 to 5.

5 = Correct, complete, and directly answers the question.
4 = Mostly correct with minor omissions.
3 = Partially correct.
2 = Mostly incorrect or missing important information.
1 = Incorrect, unsupported, or irrelevant.

Return ONLY the number.
"""

    response = llm.invoke(prompt)

    try:
        return int(response.content.strip())
    except ValueError:
        return 0


def main():

    with open(
        "tests/answer_questions.json",
        "r",
        encoding="utf-8",
    ) as f:
        dataset = json.load(f)

    parent_child = ParentChildRAG()
    multivector = MultiVectorRAG()

    pc_scores = []
    mv_scores = []

    print("=" * 80)
    print("ANSWER QUALITY EVALUATION")
    print("=" * 80)

    for index, item in enumerate(
        dataset,
        start=1,
    ):

        question = item["question"]
        reference = item["reference_answer"]

        print(
            f"\n[{index}/{len(dataset)}] "
            f"{question}"
        )

        pc_result = parent_child.ask(
            question
        )

        mv_result = multivector.ask(
            question
        )

        pc_score = evaluate_answer(
            parent_child.llm,
            question,
            reference,
            pc_result["answer"],
        )

        mv_score = evaluate_answer(
            multivector.llm,
            question,
            reference,
            mv_result["answer"],
        )

        pc_scores.append(pc_score)
        mv_scores.append(mv_score)

        print(
            f"Parent-Child score: {pc_score}/5"
        )

        print(
            f"Multi-Vector score: {mv_score}/5"
        )

    pc_average = (
        sum(pc_scores) / len(pc_scores)
    )

    mv_average = (
        sum(mv_scores) / len(mv_scores)
    )

    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    print(
        f"Parent-Child average: "
        f"{pc_average:.2f}/5"
    )

    print(
        f"Multi-Vector average: "
        f"{mv_average:.2f}/5"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()
