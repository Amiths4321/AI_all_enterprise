def citation_precision(
    cited_document_ids: list[str],
    expected_document_ids: list[str],
) -> float:

    if not cited_document_ids:
        return 0.0

    expected = set(expected_document_ids)

    correct = sum(
        1
        for document_id in cited_document_ids
        if document_id in expected
    )

    return correct / len(cited_document_ids)


def citation_recall(
    cited_document_ids: list[str],
    expected_document_ids: list[str],
) -> float:

    if not expected_document_ids:
        return 0.0

    cited = set(cited_document_ids)
    expected = set(expected_document_ids)

    return len(
        cited & expected
    ) / len(expected)

def citation_validity(
    cited_document_ids: list[str],
    available_document_ids: list[str],
) -> float:

    if not cited_document_ids:
        return 0.0

    available = set(
        available_document_ids
    )

    valid = sum(
        1
        for document_id in cited_document_ids
        if document_id in available
    )

    return valid / len(cited_document_ids)