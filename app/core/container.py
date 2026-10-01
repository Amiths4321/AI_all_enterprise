import json
from pathlib import Path
from typing import Any

from app.evaluation.evidence import SemanticEvidenceEvaluator
from app.generation.ollama import OllamaGenerator
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.reranker import CrossEncoderReranker
from app.retrieval.vector import InMemoryVectorSearcher
from app.services.rag_service import RAGService


class ApplicationContainer:

    def __init__(
        self,
        documents: list[dict[str, Any]],
        config_path: str,
    ):
        self.documents = documents

        with open(
            Path(config_path),
            "r",
            encoding="utf-8",
        ) as file:
            self.config = json.load(file)

    def build(self) -> RAGService:

        reranking_config = self.config["reranking"]

        vector_searcher = InMemoryVectorSearcher(
            documents=self.documents,
        )

        retriever = HybridRetriever(
            documents=self.documents,
            vector_searcher=vector_searcher,
        )

        reranker = CrossEncoderReranker(
            model_name=reranking_config["model"],
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