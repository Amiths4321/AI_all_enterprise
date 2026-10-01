from app.core.cache import TTLCache
from app.core.security import UserContext
from app.services.cached_retrieval import (
    CachedRetrievalService,
)


class FakeRetrieval:

    def __init__(self):
        self.calls = 0

    def retrieve(
        self,
        question,
        user,
        top_k=10,
        top_n=3,
    ):
        self.calls += 1

        return {
            "reranked": [
                {
                    "id": "hr-001",
                }
            ]
        }


def test_second_request_uses_cache():

    retrieval = FakeRetrieval()

    service = CachedRetrievalService(
        retrieval_service=retrieval,
        cache=TTLCache(),
    )

    user = UserContext(
        "user-1",
        "employee",
        "HR",
    )

    first = service.retrieve(
        "What is leave?",
        user,
    )

    second = service.retrieve(
        "What is leave?",
        user,
    )

    assert first["cache_hit"] is False
    assert second["cache_hit"] is True

    assert retrieval.calls == 1