from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self, parent_store):

        self.parent_ids = list(
            parent_store.keys()
        )

        self.documents = [
            parent_store[parent_id]["text"]
            for parent_id in self.parent_ids
        ]

        tokenized = [
            document.lower().split()
            for document in self.documents
        ]

        self.bm25 = BM25Okapi(tokenized)

    def search(
        self,
        query,
        top_k=10,
    ):

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(
                self.parent_ids,
                scores,
            ),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked[:top_k]