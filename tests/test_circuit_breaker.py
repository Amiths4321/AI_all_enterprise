import pytest

from app.core.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
)


def test_circuit_opens_after_failures():

    breaker = CircuitBreaker(
        failure_threshold=2,
    )

    def failure():
        raise RuntimeError("failure")

    with pytest.raises(RuntimeError):
        breaker.call(failure)

    with pytest.raises(RuntimeError):
        breaker.call(failure)

    assert (
        breaker.state
        == CircuitState.OPEN
    )


def test_success_keeps_circuit_closed():

    breaker = CircuitBreaker()

    result = breaker.call(
        lambda: "success"
    )

    assert result == "success"

    assert (
        breaker.state
        == CircuitState.CLOSED
    )