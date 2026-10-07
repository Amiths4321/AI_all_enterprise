from app.retrieval.parallel import ParallelRetriever


class FakeRetriever:

    def retrieve(
        self,
        question,
        top_k=10,
        filters=None,
        strategy="hybrid",
    ):
        return [
            {
                "id": question,
                "document": question,
            }
        ]


def test_parallel_retrieval():

    retriever = ParallelRetriever(
        FakeRetriever(),
        max_workers=2,
    )

    results = retriever.retrieve(
        [
            "question one",
            "question two",
        ]
    )

    assert len(results) == 2
    assert "question one" in results
    assert "question two" in results