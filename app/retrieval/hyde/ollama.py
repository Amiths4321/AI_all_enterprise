import requests

from app.retrieval.hyde.generator import (
    HypotheticalDocumentGenerator,
)


class OllamaHyDEGenerator(
    HypotheticalDocumentGenerator
):

    def __init__(
        self,
        base_url: str = "http://10.22.39.192:11434",
        model: str = "qwen2.5vl:latest",
        timeout: int = 60,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate(self, question: str) -> str:

        prompt = f"""
You are generating a hypothetical document only for
semantic retrieval.

Question:
{question}

Write a concise hypothetical passage that would likely
contain the information needed to answer the question.

Do not mention that this is hypothetical.
Do not invent citations.
Do not claim that the passage is an authoritative source.

Hypothetical passage:
""".strip()

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

        data = response.json()

        return data["response"].strip()