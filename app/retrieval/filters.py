from typing import Any


class MetadataFilter:

    def apply(
        self,
        documents: list[dict[str, Any]],
        *,
        department: str | None = None,
        document_type: str | None = None,
        year: int | None = None,
    ) -> list[dict[str, Any]]:

        filtered = []

        for item in documents:

            metadata = item.get(
                "metadata",
                {},
            )

            if (
                department is not None
                and metadata.get("department")
                != department
            ):
                continue

            if (
                document_type is not None
                and metadata.get("document_type")
                != document_type
            ):
                continue

            if (
                year is not None
                and metadata.get("year")
                != year
            ):
                continue

            filtered.append(item)

        return filtered