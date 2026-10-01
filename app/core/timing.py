from dataclasses import dataclass, field
from time import perf_counter


@dataclass
class TimingResult:
    stages: dict[str, float] = field(
        default_factory=dict
    )

    @property
    def total_ms(self) -> float:
        return sum(self.stages.values())


class StageTimer:

    def __init__(self):
        self.result = TimingResult()

    def measure(self, stage: str):

        return _TimerContext(
            self.result,
            stage,
        )


class _TimerContext:

    def __init__(
        self,
        result: TimingResult,
        stage: str,
    ):
        self.result = result
        self.stage = stage

    def __enter__(self):
        self.started = perf_counter()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        elapsed = (
            perf_counter() - self.started
        ) * 1000

        self.result.stages[
            self.stage
        ] = elapsed