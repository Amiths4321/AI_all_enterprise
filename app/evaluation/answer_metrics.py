from sentence_transformers import SentenceTransformer


class AnswerSimilarityEvaluator:

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(
            model_name
        )

    def score(
        self,
        answer: str,
        reference_answer: str,
    ) -> float:

        embeddings = self.model.encode(
            [
                answer,
                reference_answer,
            ]
        )

        similarity = (
            embeddings[0] @ embeddings[1]
        )

        norm = (
            (
                embeddings[0] ** 2
            ).sum() ** 0.5
            *
            (
                embeddings[1] ** 2
            ).sum() ** 0.5
        )

        if norm == 0:
            return 0.0

        return float(similarity / norm)