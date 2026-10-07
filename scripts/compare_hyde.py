from app.retrieval.hyde.retriever import HyDERetriever


def evaluate_retriever(
    name,
    retriever,
    cases,
):

    hits = 0

    for case in cases:

        result = retriever.retrieve(
            case["question"],
            top_k=5,
        )

        if hasattr(result, "documents"):
            documents = result.documents
        else:
            documents = result

        ids = {
            document["id"]
            for document in documents
        }

        expected = set(
            case["expected_document_ids"]
        )

        if ids.intersection(expected):
            hits += 1

    score = (
        hits / len(cases)
        if cases
        else 0.0
    )

    print(
        f"{name}: "
        f"hit-rate@5={score:.3f}"
    )