from typing import Any

from app.query.planner import AdvancedQueryPlanner


class MultiQueryRetriever:

    def __init__(
        self,
        planner: AdvancedQueryPlanner,
        retriever,
    ):
        self.planner = planner
        self.retriever = retriever

    def retrieve(
        self,
        question: str,
        top_k: int = 10,
        filters: dict | None = None,
        strategy: str = "hybrid",
    ) -> list[dict[str, Any]]:

        plan = self.planner.plan(question)

        documents = {}
        
        for query in plan.retrieval_queries:

            results = self.retriever.retrieve(
                query,
                top_k=top_k,
                filters=filters or {},
                strategy=strategy,
            )

            for document in results:
                document_id = document["id"]
                documents[document_id] = document

        return list(documents.values())