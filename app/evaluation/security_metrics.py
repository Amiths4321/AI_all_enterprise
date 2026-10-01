def security_leakage_count(
    returned_document_ids: list[str],
    authorized_document_ids: list[str],
) -> int:

    authorized = set(
        authorized_document_ids
    )

    return sum(
        1
        for document_id in returned_document_ids
        if document_id not in authorized
    )


def security_passed(
    returned_document_ids: list[str],
    authorized_document_ids: list[str],
) -> bool:

    return (
        security_leakage_count(
            returned_document_ids,
            authorized_document_ids,
        )
        == 0
    )