class RetrievalFailureAnalyzer:

    def classify(
        self,
        retrieved_ids: list[str],
        expected_ids: list[str],
    ) -> str:

        if not retrieved_ids:
            return "no_retrieval"

        if not expected_ids:
            return "invalid_expected_set"

        retrieved = set(retrieved_ids)
        expected = set(expected_ids)

        if retrieved.intersection(expected):
            return "success"

        return "miss"