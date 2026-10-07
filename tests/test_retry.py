from app.core.retry import (
    RetryPolicy,
)


def test_retry_eventually_succeeds():

    attempts = {
        "count": 0
    }

    def operation():

        attempts["count"] += 1

        if attempts["count"] < 3:
            raise RuntimeError(
                "temporary"
            )

        return "success"

    policy = RetryPolicy(
        max_attempts=3,
        base_delay_seconds=0,
    )

    result = policy.execute(
        operation
    )

    assert result == "success"
    assert attempts["count"] == 3