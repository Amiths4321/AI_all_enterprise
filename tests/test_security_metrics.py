from app.evaluation.security_metrics import (
    security_leakage_count,
    security_passed,
)


def test_no_security_leakage():

    assert security_leakage_count(
        ["hr-001"],
        ["hr-001"],
    ) == 0

    assert security_passed(
        ["hr-001"],
        ["hr-001"],
    )


def test_security_leakage():

    assert security_leakage_count(
        ["hr-001", "finance-001"],
        ["hr-001"],
    ) == 1

    assert not security_passed(
        ["hr-001", "finance-001"],
        ["hr-001"],
    )