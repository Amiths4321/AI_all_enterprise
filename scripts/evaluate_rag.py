import json
from pathlib import Path
import sys

# Adds the project root directory to Python's module path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.rag.pipeline import ParentChildRAG

# Rest of your evaluation code...

from src.rag.pipeline import ParentChildRAG


def main():

    with open(
        "tests/rag_questions.json",
        "r",
        encoding="utf-8",
    ) as f:
        questions = json.load(f)

    rag = ParentChildRAG()

    for index, item in enumerate(
        questions,
        start=1,
    ):

        question = item["question"]
        reference = item["reference"]

        result = rag.ask(question)

        print("\n" + "=" * 80)
        print(f"QUESTION {index}")
        print("=" * 80)

        print(question)

        print("\nREFERENCE ANSWER")
        print("-" * 80)

        print(reference)

        print("\nMODEL ANSWER")
        print("-" * 80)

        print(result["answer"])

        print("\nSOURCES")
        print("-" * 80)

        for source in result["sources"]:

            print(
                f"{source['parent_id']} | "
                f"retrieval={source['retrieval_score']:.4f} | "
                f"reranker={source['reranker_score']:.4f}"
            )


if __name__ == "__main__":
    main()