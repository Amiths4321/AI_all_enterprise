import json

from app.retrieval.repository import DocumentRepository


def test_document_repository(tmp_path):

    path = tmp_path / "documents.json"

    documents = [
        {
            "id": "doc-1",
            "document": "Test document",
            "metadata": {
                "source": "test.txt"
            },
        }
    ]

    path.write_text(
        json.dumps(documents),
        encoding="utf-8",
    )

    repository = DocumentRepository(
        path=str(path)
    )

    repository.load()

    assert repository.count() == 1

    assert (
        repository.get_all()[0]["id"]
        == "doc-1"
    )