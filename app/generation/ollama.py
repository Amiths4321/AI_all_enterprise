import os
import requests


class OllamaGenerator:

    def __init__(
        self,
        base_url=None,
        model=None,
        timeout=120,
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
        prompt: str,
        documents=None,
    ) -> str:

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