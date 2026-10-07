from app.core.metrics import (
    RequestMetrics,
)
from app.core.slo import (
    SLOEvaluator,
)


def test_healthy_slo():

    metrics = RequestMetrics()

    metrics.record_success(
        1000
    )

    metrics.cache_hits = 5
    metrics.cache_misses = 5

    result = SLOEvaluator().evaluate(
        metrics
    )

    assert result["healthy"] is True


def test_error_rate_failure():

    metrics = RequestMetrics()

    for _ in range(100):
        metrics.record_success(100)

    for _ in range(5):
        metrics.record_failure(100)

    result = SLOEvaluator().evaluate(
        metrics
    )

    assert result["healthy"] is False
    assert "error_rate" in result[
        "failures"
    ]