from app.retrieval.rrf import RRFFuser


def test_rrf_fuses_multiple_rankings():

    rankings = [
        [
            {"id": "A", "document": "Document A"},
            {"id": "B", "document": "Document B"},
            {"id": "C", "document": "Document C"},
        ],
        [
            {"id": "B", "document": "Document B"},
            {"id": "D", "document": "Document D"},
            {"id": "A", "document": "Document A"},
        ],
        [
            {"id": "A", "document": "Document A"},
            {"id": "D", "document": "Document D"},
            {"id": "E", "document": "Document E"},
        ],
    ]

    fuser = RRFFuser(k=60)

    result = fuser.fuse(rankings)

    ids = [document["id"] for document in result]

    assert ids[0] == "A"


def test_rrf_adds_scores():

    rankings = [
        [{"id": "A", "document": "A"}],
        [{"id": "A", "document": "A"}],
    ]

    fuser = RRFFuser(k=60)

    result = fuser.fuse(rankings)

    assert result[0]["rrf_score"] > 0