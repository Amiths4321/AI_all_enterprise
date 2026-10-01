from typing import Any

from app.core.container import ApplicationContainer
from app.services.rag_service import RAGService


class Application:

    def __init__(
        self,
        documents: list[dict[str, Any]],
        config_path: str,
    ):
        self.documents = documents
        self.config_path = config_path
        self.rag_service: RAGService | None = None

    def startup(self) -> None:

        container = ApplicationContainer(
            documents=self.documents,
            config_path=self.config_path,
        )

        self.rag_service = container.build()

    def get_rag_service(self) -> RAGService:

        if self.rag_service is None:
            raise RuntimeError(
                "Application has not been started."
            )

        return self.rag_service