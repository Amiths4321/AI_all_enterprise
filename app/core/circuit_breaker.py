from enum import Enum
from time import monotonic


class CircuitState(Enum):

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:

    def __init__(
        self,
        failure_threshold=3,
        recovery_timeout=30,
    ):
        self.failure_threshold = (
            failure_threshold
        )

        self.recovery_timeout = (
            recovery_timeout
        )

        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None

    def _can_attempt(self):

        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:

            elapsed = (
                monotonic()
                - self.opened_at
            )

            if elapsed >= (
                self.recovery_timeout
            ):
                self.state = (
                    CircuitState.HALF_OPEN
                )
                return True

            return False

        return True

    def call(self, operation):

        if not self._can_attempt():

            raise RuntimeError(
                "Circuit is open"
            )

        try:

            result = operation()

            self.failure_count = 0
            self.state = (
                CircuitState.CLOSED
            )

            return result

        except Exception:

            self.failure_count += 1

            if (
                self.failure_count
                >= self.failure_threshold
            ):

                self.state = (
                    CircuitState.OPEN
                )

                self.opened_at = monotonic()

            raise