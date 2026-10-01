import json

from app.core.container import ApplicationContainer
from app.services.rag_service import RAGService


class Application:

    def __init__(
        self,
        config_path: str,
    ):
        self.config_path = config_path
        self.rag_service: RAGService | None = None
        self.repository = None

    def startup(self) -> None:

        with open(
            self.config_path,
            "r",
            encoding="utf-8",
        ) as file:
            config = json.load(file)

        container = ApplicationContainer(
            config=config,
        )

        self.repository = (
            container.build_repository()
        )

        self.rag_service = container.build()

    def get_rag_service(self) -> RAGService:

        if self.rag_service is None:
            raise RuntimeError(
                "Application has not been started."
            )

        return self.rag_service

    def is_ready(self) -> bool:

        if self.rag_service is None:
            return False

        if self.repository is None:
            return False

        return self.repository.count() > 0