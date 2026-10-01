from typing import Any

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from app.core.interfaces import EvidenceEvaluator


MODEL_NAME = "all-MiniLM-L6-v2"


class SemanticEvidenceEvaluator(EvidenceEvaluator):
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def evaluate(
        self,
        required_evidence: list[str],
        retrieved_documents: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not required_evidence:
            return {
                "evidence_recall": 1.0,
                "matches": [],
            }

        if not retrieved_documents:
            return {
                "evidence_recall": 0.0,
                "matches": [],
            }

        documents = [
            item["document"]
            for item in retrieved_documents
        ]

        document_embeddings = self.model.encode(
            documents,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        matches = []
        found = 0

        for evidence in required_evidence:

            evidence_embedding = self.model.encode(
                evidence,
                convert_to_tensor=True,
                normalize_embeddings=True,
            )

            scores = cos_sim(
                evidence_embedding,
                document_embeddings,
            )[0]

            best_index = int(scores.argmax().item())
            best_score = float(
                scores[best_index].item()
            )

            best_document = retrieved_documents[best_index]

            matches.append(
                {
                    "evidence": evidence,
                    "score": best_score,
                    "document_id": best_document["id"],
                    "source": best_document
                    .get("metadata", {})
                    .get("source"),
                }
            )

            if best_score >= 0.60:
                found += 1

        return {
            "evidence_recall": (
                found / len(required_evidence)
            ),
            "matches": matches,
        }