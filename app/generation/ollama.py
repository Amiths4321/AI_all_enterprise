import os
from typing import Any

import requests

from app.core.interfaces import Generator


class OllamaGenerator(Generator):
    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = 120,
    ):
        self.base_url = (
            base_url
            or os.getenv(
                "OLLAMA_URL",
                "http://10.22.39.192:11434",
            )
        )

        self.model = (
            model
            or os.getenv(
                "OLLAMA_MODEL",
                "qwen2.5vl:latest",
            )
        )

        self.timeout = timeout

    def generate(
        self,
        question: str,
        documents: list[dict[str, Any]],
    ) -> str:

        context_parts = []

        for index, item in enumerate(
            documents,
            start=1,
        ):
            source = (
                item.get("metadata", {})
                .get("source", "unknown")
            )

            context_parts.append(
                f"[SOURCE {index}: {source}]\n"
                f"{item['document']}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are a retrieval-grounded enterprise assistant.

Answer the question using ONLY the supplied context.

Rules:
1. Do not use outside knowledge.
2. Do not invent facts.
3. If the context does not contain enough evidence, say:
   "I don't have enough information in the provided documents."
4. Keep the answer concise.
5. Cite the source names used in your answer.

Question:
{question}

Context:
{context}

Answer:
"""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()["response"]