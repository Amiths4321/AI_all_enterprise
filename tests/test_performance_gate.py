from app.evaluation.performance_gate import (
    PerformanceQualityGate,
)


def test_performance_gate_passes():

    result = PerformanceQualityGate().validate(
        p95_latency_ms=1000,
        p99_latency_ms=2000,
        cache_hit_rate=0.50,
    )

    assert result["passed"] is True


def test_p95_failure():

    result = PerformanceQualityGate().validate(
        p95_latency_ms=5000,
        p99_latency_ms=2000,
        cache_hit_rate=0.50,
    )

    assert result["passed"] is False
    assert "p95_latency" in result[
        "failures"
    ]