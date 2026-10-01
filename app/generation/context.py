from dataclasses import dataclass


@dataclass(frozen=True)
class ContextDocument:
    number: int
    document_id: str
    text: str
    source: str | None


class ContextBuilder:

    def build(self, documents: list[dict]) -> list[ContextDocument]:
        context = []

        for index, document in enumerate(documents, start=1):
            metadata = document.get("metadata", {})

            context.append(
                ContextDocument(
                    number=index,
                    document_id=document["id"],
                    text=document.get("document", ""),
                    source=metadata.get("source"),
                )
            )

        return context

class ContextRenderer:

    def render(
        self,
        documents: list[ContextDocument],
    ) -> str:

        sections = []

        for document in documents:
            source = document.source or "unknown"

            sections.append(
                f"[{document.number}] "
                f"Document ID: {document.document_id}\n"
                f"Source: {source}\n"
                f"Content: {document.text}"
            )

        return "\n\n".join(sections)