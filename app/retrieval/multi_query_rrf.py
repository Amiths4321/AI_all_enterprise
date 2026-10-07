from typing import Any

from app.query.planner import AdvancedQueryPlanner
from app.retrieval.rrf import RRFFuser


class MultiQueryRRFRetriever:

    def __init__(
        self,
        planner: AdvancedQueryPlanner,
        retriever,
        fuser: RRFFuser,
    ):
        self.planner = planner
        self.retriever = retriever
        self.fuser = fuser

    def retrieve(
        self,
        question: str,
        top_k: int = 10,
        filters: dict | None = None,
        strategy: str = "hybrid",
    ) -> list[dict[str, Any]]:

        plan = self.planner.plan(question)

        rankings = []
        query_names = []

        for index, query in enumerate(
            plan.retrieval_queries,
            start=1,
        ):

            results = self.retriever.retrieve(
                query,
                top_k=top_k,
                filters=filters or {},
                strategy=strategy,
            )

            rankings.append(results)

            query_names.append(
                f"query-{index}"
            )

        if not rankings:
            return []

        return self.fuser.fuse(
            rankings,
            query_names=query_names,
        )