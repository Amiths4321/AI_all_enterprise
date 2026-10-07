from typing import Any


def attach_query_provenance(
    documents: list[dict[str, Any]],
    query_id: str,
    query: str,
) -> list[dict[str, Any]]:

    enriched = []

    for document in documents:

        item = dict(document)

        item["query_provenance"] = {
            "query_id": query_id,
            "query": query,
        }

        enriched.append(item)

    return enriched