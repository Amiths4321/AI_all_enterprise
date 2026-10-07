from dataclasses import dataclass


@dataclass(frozen=True)
class HyDERetrievalResult:
    question: str
    hypothetical_document: str
    documents: list[dict]