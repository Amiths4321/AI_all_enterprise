import json
from pathlib import Path
from typing import Any


class DocumentRepository:

    def __init__(self, path: str):
        self.path = Path(path)
        self.documents: list[dict[str, Any]] = []

    def load(self) -> None:
        with self.path.open(
            "r",
            encoding="utf-8",
        ) as file:
            self.documents = json.load(file)

    def get_all(self) -> list[dict[str, Any]]:
        return self.documents

    def count(self) -> int:
        return len(self.documents)