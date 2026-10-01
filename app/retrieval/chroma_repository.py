from typing import Any

import chromadb

from app.core.interfaces import DocumentRepository
   

class ChromaDocumentRepository(DocumentRepository):

    def __init__(
        self,
        path: str,
        collection_name: str = "enterprise_documents",
    ):
        self.client = chromadb.PersistentClient(
            path=path
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def get_all(self) -> list[dict[str, Any]]:

        result = self.collection.get(
            include=["documents", "metadatas"],
        )

        documents = []

        ids = result.get("ids", [])
        texts = result.get("documents", [])
        metadatas = result.get("metadatas", [])

        for index, document_id in enumerate(ids):

            documents.append(
                {
                    "id": document_id,
                    "document": texts[index],
                    "metadata": (
                        metadatas[index]
                        if metadatas[index]
                        else {}
                    ),
                }
            )

        return documents

    def count(self) -> int:
        return self.collection.count()

    def add_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> None:
        
        # Helper function to sanitize metadata values for ChromaDB (no lists allowed)
        def sanitize_metadata(meta: dict[str, Any]) -> dict[str, Any]:
            if not meta:
                return {}
            cleaned = {}
            for key, value in meta.items():
                if isinstance(value, list):
                    # Convert lists (like ['employee', 'manager']) into comma-separated strings
                    cleaned[key] = ", ".join(str(v) for v in value)
                else:
                    cleaned[key] = value
            return cleaned

        self.collection.upsert(
            ids=[
                item["id"]
                for item in documents
            ],
            documents=[
                item["document"]
                for item in documents
            ],
            metadatas=[
                sanitize_metadata(item.get("metadata", {}))
                for item in documents
            ]
        )



            