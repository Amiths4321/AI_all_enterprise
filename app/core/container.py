from typing import Any

from app.evaluation.evidence import SemanticEvidenceEvaluator
from app.generation.ollama import OllamaGenerator
from app.retrieval.chroma_repository import (
    ChromaDocumentRepository,
)
from app.retrieval.chroma_vector import (
    ChromaVectorSearcher,
)
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.reranker import CrossEncoderReranker
from app.services.rag_service import RAGService


class ApplicationContainer:

    def __init__(
        self,
        config: dict[str, Any],
    ):
        self.config = config

    def build_repository(
        self,
    ) -> ChromaDocumentRepository:

        storage = self.config["storage"]

        return ChromaDocumentRepository(
            path=storage["path"],
            collection_name=storage["collection"],
        )

    def build(self) -> RAGService:

        repository = self.build_repository()

        vector_searcher = ChromaVectorSearcher(
            repository=repository,
        )

        retriever = HybridRetriever(
            documents=repository.get_all(),
            vector_searcher=vector_searcher,
        )

        reranker_config = self.config["reranking"]

        reranker = CrossEncoderReranker(
            model_name=reranker_config["model"],
        )

        evidence_evaluator = SemanticEvidenceEvaluator()

        generator = OllamaGenerator(
            timeout=self.config["generation"]["timeout"],
        )

        return RAGService(
            retriever=retriever,
            reranker=reranker,
            evidence_evaluator=evidence_evaluator,
            generator=generator,
        )