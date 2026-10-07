from dataclasses import dataclass
import requests


@dataclass
class DependencyHealth:
    name: str
    healthy: bool
    detail: str


class HealthChecker:

    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def check_ollama(self, generator) -> DependencyHealth:
        try:
            response = generator.health()
            return DependencyHealth(
                name="ollama",
                healthy=response,
                detail="available" if response else "unavailable",
            )
        except Exception as exc:
            return DependencyHealth(
                name="ollama",
                healthy=False,
                detail=str(exc),
            )

    def check_repository(self, repository) -> DependencyHealth:
        try:
            count = repository.count()
            return DependencyHealth(
                name="chroma",
                healthy=True,
                detail=f"documents={count}",
            )
        except Exception as exc:
            return DependencyHealth(
                name="chroma",
                healthy=False,
                detail=str(exc),
            )

    def health(self) -> bool:
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5,
            )
            return response.ok
        except requests.RequestException:
            return False