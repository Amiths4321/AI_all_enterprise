from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    def __init__(
        self,
        model_name=(
            "cross-encoder/"
            "ms-marco-MiniLM-L-6-v2"
        ),
    ):
        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        question,
        documents,
        top_n=3,
    ):

        if not documents:
            return []

        pairs = [
            (
                question,
                document.get(
                    "document",
                    "",
                ),
            )
            for document in documents
        ]

        scores = self.model.predict(
            pairs,
            batch_size=32,
        )

        ranked = []

        for document, score in zip(
            documents,
            scores,
        ):
            item = dict(document)
            item["rerank_score"] = float(
                score
            )
            ranked.append(item)

        ranked.sort(
            key=lambda item: item[
                "rerank_score"
            ],
            reverse=True,
        )

        return ranked[:top_n]