class EvidenceAggregator:

    def aggregate(
        self,
        evidence_sets: list[list[dict]],
    ) -> list[dict]:

        documents = {}

        for evidence_set in evidence_sets:

            for document in evidence_set:

                document_id = document["id"]

                if document_id not in documents:
                    documents[document_id] = (
                        document
                    )

        return list(
            documents.values()
        )