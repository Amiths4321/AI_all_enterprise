from app.query.query_relationship import QueryRelationship


class QueryRelationshipClassifier:

    def classify(
        self,
        original_question: str,
        sub_questions: list[str],
    ) -> QueryRelationship:

        text = original_question.lower()

        if any(
            word in text
            for word in [
                "compare",
                "comparison",
                "difference",
                "versus",
                "vs",
            ]
        ):
            return QueryRelationship.COMPARISON

        if any(
            phrase in text
            for phrase in [
                "after that",
                "then",
                "once they",
                "after they",
                "based on the result",
            ]
        ):
            return QueryRelationship.DEPENDENT

        return QueryRelationship.INDEPENDENT