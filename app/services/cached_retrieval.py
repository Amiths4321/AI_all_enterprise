from app.core.cache_key import (
    build_cache_key,
)


class CachedRetrievalService:

    def __init__(
        self,
        retrieval_service,
        cache,
    ):
        self.retrieval_service = (
            retrieval_service
        )
        self.cache = cache

    def retrieve(
        self,
        question,
        user,
        top_k=10,
        top_n=3,
    ):

        key = build_cache_key(
            question=question,
            user_id=user.user_id,
            role=user.role,
            department=user.department,
            top_k=top_k,
            top_n=top_n,
        )

        cached = self.cache.get(key)

        if cached is not None:

            return {
                **cached,
                "cache_hit": True,
            }

        result = self.retrieval_service.retrieve(
            question=question,
            user=user,
            top_k=top_k,
            top_n=top_n,
        )

        self.cache.set(
            key,
            result,
        )

        return {
            **result,
            "cache_hit": False,
        }