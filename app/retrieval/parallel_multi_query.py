from app.query.dependency_planner import (
    QueryDependencyPlanner,
)
from app.query.planner import AdvancedQueryPlanner
from app.retrieval.parallel import ParallelRetriever
from app.retrieval.rrf import RRFFuser


class ParallelMultiQueryRetriever:

    def __init__(
        self,
        planner: AdvancedQueryPlanner,
        dependency_planner: QueryDependencyPlanner,
        parallel_retriever: ParallelRetriever,
        fuser: RRFFuser,
    ):
        self.planner = planner
        self.dependency_planner = dependency_planner
        self.parallel_retriever = parallel_retriever
        self.fuser = fuser

    def retrieve(
        self,
        question: str,
        top_k: int = 10,
        filters: dict | None = None,
        strategy: str = "hybrid",
    ):

        plan = self.planner.plan(question)

        nodes = self.dependency_planner.plan(plan)

        independent = [
            node
            for node in nodes
            if not node.depends_on
        ]

        if not independent:
            return []

        questions = [
            node.question
            for node in independent
        ]

        results = self.parallel_retriever.retrieve(
            questions,
            top_k=top_k,
            filters=filters,
            strategy=strategy,
        )

        rankings = [
            results[node.question]
            for node in independent
        ]

        query_names = [
            node.query_id
            for node in independent
        ]

        return self.fuser.fuse(
            rankings,
            query_names=query_names,
        )