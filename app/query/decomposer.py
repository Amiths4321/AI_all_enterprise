import re


class QueryDecomposer:

    def decompose(self, question: str) -> list[str]:

        text = question.strip()

        if not text:
            return []

        parts = re.split(
            r"\s+(?:and|also)\s+",
            text,
            flags=re.IGNORECASE,
        )

        parts = [
            part.strip(" ?.")
            for part in parts
            if part.strip()
        ]

        if len(parts) == 1:
            return [text]

        return parts