from rank_bm25 import BM25Okapi


class HybridRetriever:

    def __init__(self, vectorstore, parent_store):
        self.vectorstore = vectorstore
        self.parent_store = parent_store

        self.parent_ids = list(parent_store.keys())

        self.documents = [
            parent_store[parent_id]["text"]
            for parent_id in self.parent_ids
        ]

        tokenized = [
            text.lower().split()
            for text in self.documents
        ]

        self.bm25 = BM25Okapi(tokenized)

    def vector_search(self, query, k=20):
        return self.vectorstore.similarity_search_with_score(
            query,
            k=k,
        )

    def keyword_search(self, query, k=10):
        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(self.parent_ids, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked[:k]

    def search(self, query, vector_k=20, keyword_k=10):

        vector_results = self.vector_search(
            query,
            vector_k,
        )

        keyword_results = self.keyword_search(
            query,
            keyword_k,
        )

        return {
            "vector": vector_results,
            "keyword": keyword_results,
        }