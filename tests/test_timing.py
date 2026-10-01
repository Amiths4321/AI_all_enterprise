import time

from app.core.timing import StageTimer


def test_stage_timer():

    timer = StageTimer()

    with timer.measure("test"):
        time.sleep(0.01)

    assert "test" in timer.result.stages
    assert timer.result.stages["test"] > 0
    assert timer.result.total_ms > 0