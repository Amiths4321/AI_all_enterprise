from app.core.cache_key import (
    build_cache_key,
)


def test_same_user_same_request_same_key():

    first = build_cache_key(
        "What is the policy?",
        "user-1",
        "employee",
        "HR",
        10,
        3,
    )

    second = build_cache_key(
        "What is the policy?",
        "user-1",
        "employee",
        "HR",
        10,
        3,
    )

    assert first == second


def test_different_users_have_different_keys():

    first = build_cache_key(
        "What is the policy?",
        "user-1",
        "employee",
        "HR",
        10,
        3,
    )

    second = build_cache_key(
        "What is the policy?",
        "user-2",
        "employee",
        "HR",
        10,
        3,
    )

    assert first != second


def test_different_departments_have_different_keys():

    hr = build_cache_key(
        "What is the policy?",
        "user-1",
        "employee",
        "HR",
        10,
        3,
    )

    finance = build_cache_key(
        "What is the policy?",
        "user-1",
        "employee",
        "Finance",
        10,
        3,
    )

    assert hr != finance