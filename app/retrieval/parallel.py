from concurrent.futures import ThreadPoolExecutor
from typing import Any


class ParallelRetriever:

    def __init__(
        self,
        retriever,
        max_workers: int = 4,
    ):
        if max_workers <= 0:
            raise ValueError(
                "max_workers must be positive"
            )

        self.retriever = retriever
        self.max_workers = max_workers

    def retrieve(
        self,
        questions: list[str],
        top_k: int = 10,
        filters: dict | None = None,
        strategy: str = "hybrid",
    ) -> dict[str, list[dict[str, Any]]]:

        if not questions:
            return {}

        def retrieve_one(question: str):
            return self.retriever.retrieve(
                question,
                top_k=top_k,
                filters=filters or {},
                strategy=strategy,
            )

        with ThreadPoolExecutor(
            max_workers=min(
                self.max_workers,
                len(questions),
            )
        ) as executor:

            results = executor.map(
                retrieve_one,
                questions,
            )

        return dict(
            zip(questions, results)
        )