import json
from pathlib import Path

from app.retrieval.chroma_repository import (
    ChromaDocumentRepository,
)


DOCUMENT_FILE = Path("data/documents.json")
CHROMA_PATH = "chroma_db"


with DOCUMENT_FILE.open(
    "r",
    encoding="utf-8",
) as file:
    documents = json.load(file)


repository = ChromaDocumentRepository(
    path=CHROMA_PATH,
)

repository.add_documents(documents)

print(
    f"Loaded {repository.count()} documents "
    "into Chroma."
)