import re


class CitationExtractor:

    PATTERN = re.compile(r"\[(\d+)\]")

    def extract(self, answer: str) -> list[int]:
        citations = self.PATTERN.findall(answer)

        return sorted(
            set(int(value) for value in citations)
        )

class CitationVerifier:

    def verify(
        self,
        answer: str,
        documents,
    ) -> dict:

        citations = CitationExtractor().extract(answer)

        valid_numbers = {
            document.number
            for document in documents
        }

        invalid = [
            citation
            for citation in citations
            if citation not in valid_numbers
        ]

        return {
            "citations": citations,
            "invalid_citations": invalid,
            "valid": len(invalid) == 0,
        }