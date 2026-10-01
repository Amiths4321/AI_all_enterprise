from app.retrieval.repository import DocumentRepository


def test_document_repository():

    documents = [
        {
            "id": "doc-1",
            "document": "Test document",
            "metadata": {
                "source": "test.txt"
            },
        }
    ]

    repository = DocumentRepository(
        documents=documents
    )

    assert repository.count() == 1
    assert repository.get_all()[0]["id"] == "doc-1"