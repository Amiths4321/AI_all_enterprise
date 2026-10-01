from app.agent.tools import AgentTool


class RetrievalTool(AgentTool):

    name = "enterprise_retrieval"

    def __init__(
        self,
        retrieval_service,
    ):
        self.retrieval_service = (
            retrieval_service
        )

    def execute(
        self,
        question: str,
        user,
    ) -> list[dict]:

        result = (
            self.retrieval_service.retrieve(
                question=question,
                user=user,
                top_k=10,
                top_n=3,
            )
        )

        return result["reranked"]