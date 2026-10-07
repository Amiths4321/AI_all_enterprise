from dataclasses import dataclass


@dataclass(frozen=True)
class SLOTargets:

    max_error_rate: float = 0.01

    max_average_latency_ms: float = 3000

    min_cache_hit_rate: float = 0.20


class SLOEvaluator:

    def __init__(
        self,
        targets=None,
    ):

        self.targets = (
            targets
            or SLOTargets()
        )

    def evaluate(
        self,
        metrics,
    ):

        failures = []

        if (
            metrics.error_rate
            > self.targets.max_error_rate
        ):
            failures.append(
                "error_rate"
            )

        if (
            metrics.average_latency_ms
            > self.targets.max_average_latency_ms
        ):
            failures.append(
                "average_latency"
            )

        if (
            metrics.cache_hit_rate
            < self.targets.min_cache_hit_rate
        ):
            failures.append(
                "cache_hit_rate"
            )

        return {
            "healthy": not failures,
            "failures": failures,
        }