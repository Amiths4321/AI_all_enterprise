from src.rag.pipeline import ParentChildRAG


def test_pipeline_initializes():

    rag = ParentChildRAG()

    assert rag.vectorstore is not None
    assert rag.llm is not None
    assert rag.reranker is not None


def test_retrieval_returns_results():

    rag = ParentChildRAG()

    results = rag.retrieve(
        "What is the purpose of the book?",
        k=5,
    )

    assert len(results) > 0


def test_parent_scoring():

    rag = ParentChildRAG()

    results = rag.retrieve(
        "What is the purpose of the book?",
        k=10,
    )

    parents = rag.score_parents(results)

    assert len(parents) > 0
    assert "parent_id" in parents[0]
    assert "score" in parents[0]