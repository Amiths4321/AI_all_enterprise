from sentence_transformers import CrossEncoder


class LocalReranker:
    def __init__(
        self,
        model_name="BAAI/bge-reranker-base",
    ):
        print(f"Loading reranker: {model_name}")

        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query,
        documents,
        top_k=3,
    ):
        if not documents:
            return []

        pairs = [
            (query, document)
            for document in documents
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(documents, scores),
            key=lambda item: float(item[1]),
            reverse=True,
        )

        return ranked[:top_k]