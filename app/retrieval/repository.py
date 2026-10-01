from typing import Any


class DocumentRepository:

    def __init__(self, documents: list[dict[str, Any]]):
        self.documents = documents

    def get_all(self) -> list[dict[str, Any]]:
        return self.documents

    def count(self) -> int:
        return len(self.documents)