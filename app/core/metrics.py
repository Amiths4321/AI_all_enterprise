from dataclasses import dataclass


@dataclass
class RequestMetrics:

    requests_total: int = 0
    requests_failed: int = 0

    total_latency_ms: float = 0.0

    cache_hits: int = 0
    cache_misses: int = 0

    retrieval_failures: int = 0
    generation_failures: int = 0
    security_failures: int = 0

    def record_success(
        self,
        latency_ms: float,
    ):

        self.requests_total += 1
        self.total_latency_ms += latency_ms

    def record_failure(
        self,
        latency_ms: float,
    ):

        self.requests_total += 1
        self.requests_failed += 1
        self.total_latency_ms += latency_ms

    @property
    def error_rate(self):

        if self.requests_total == 0:
            return 0.0

        return (
            self.requests_failed
            / self.requests_total
        )

    @property
    def average_latency_ms(self):

        if self.requests_total == 0:
            return 0.0

        return (
            self.total_latency_ms
            / self.requests_total
        )

    @property
    def cache_hit_rate(self):

        total = (
            self.cache_hits
            + self.cache_misses
        )

        if total == 0:
            return 0.0

        return (
            self.cache_hits / total
        )