from app.query.models import QueryIntent


class AdvancedIntentClassifier:

    def classify(self, question: str) -> list[QueryIntent]:

        text = question.lower()
        results = []

        if any(
            word in text
            for word in ["how many", "what", "which", "when", "where"]
        ):
            results.append(
                QueryIntent(
                    intent="factual",
                    confidence=0.9,
                )
            )

        if any(
            word in text
            for word in ["how", "process", "steps", "procedure"]
        ):
            results.append(
                QueryIntent(
                    intent="procedural",
                    confidence=0.9,
                )
            )

        if any(
            word in text
            for word in ["compare", "difference", "versus", "vs"]
        ):
            results.append(
                QueryIntent(
                    intent="comparison",
                    confidence=0.9,
                )
            )

        if not results:
            results.append(
                QueryIntent(
                    intent="general",
                    confidence=0.5,
                )
            )

        return results