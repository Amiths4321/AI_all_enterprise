import time

from app.core.cache import TTLCache


def test_cache_set_and_get():

    cache = TTLCache(
        ttl_seconds=10
    )

    cache.set(
        "question",
        "result",
    )

    assert cache.get(
        "question"
    ) == "result"


def test_cache_miss():

    cache = TTLCache()

    assert cache.get(
        "missing"
    ) is None


def test_cache_expires():

    cache = TTLCache(
        ttl_seconds=0.01
    )

    cache.set(
        "question",
        "result",
    )

    time.sleep(0.02)

    assert cache.get(
        "question"
    ) is None


def test_cache_clear():

    cache = TTLCache()

    cache.set(
        "a",
        1,
    )

    cache.clear()

    assert len(cache) == 0