from app.query.limits import QueryLimits


def test_query_limits():

    limits = QueryLimits()

    assert limits.max_sub_questions == 5
    assert limits.max_parallel_queries == 4