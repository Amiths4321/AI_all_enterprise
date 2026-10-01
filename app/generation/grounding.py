import re


class GroundingChecker:

    def check(self, answer: str) -> dict:

        sentences = [
            sentence.strip()
            for sentence in re.split(
                r"(?<=[.!?])\s+",
                answer.strip(),
            )
            if sentence.strip()
        ]

        uncited = []

        for sentence in sentences:

            if (
                sentence
                and not re.search(
                    r"\[\d+\]",
                    sentence,
                )
                and not sentence.lower().startswith(
                    (
                        "i don't",
                        "i do not",
                        "there is insufficient",
                    )
                )
            ):
                uncited.append(sentence)

        return {
            "grounded": len(uncited) == 0,
            "uncited_sentences": uncited,
        }