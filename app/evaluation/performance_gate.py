from dataclasses import dataclass


@dataclass(frozen=True)
class PerformanceThresholds:

    max_p95_latency_ms: float = 3000
    max_p99_latency_ms: float = 5000
    min_cache_hit_rate: float = 0.20


class PerformanceQualityGate:

    def __init__(
        self,
        thresholds=None,
    ):
        self.thresholds = (
            thresholds
            or PerformanceThresholds()
        )

    def validate(
        self,
        p95_latency_ms: float,
        p99_latency_ms: float,
        cache_hit_rate: float,
    ) -> dict:

        failures = []

        if (
            p95_latency_ms
            > self.thresholds.max_p95_latency_ms
        ):
            failures.append(
                "p95_latency"
            )

        if (
            p99_latency_ms
            > self.thresholds.max_p99_latency_ms
        ):
            failures.append(
                "p99_latency"
            )

        if (
            cache_hit_rate
            < self.thresholds.min_cache_hit_rate
        ):
            failures.append(
                "cache_hit_rate"
            )

        return {
            "passed": not failures,
            "failures": failures,
        }