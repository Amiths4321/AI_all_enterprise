from app.core.security import (
    AccessPolicy,
    UserContext,
)


def test_hr_employee_can_access_hr_employee_document():

    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    document = {
        "id": "hr-001",
        "metadata": {
            "department": "HR",
            "access_level": "employee",
            "allowed_roles": [
                "employee",
                "manager",
            ],
        },
    }

    policy = AccessPolicy()

    assert policy.can_access(
        user,
        document,
    )


def test_hr_employee_cannot_access_finance_document():

    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    document = {
        "id": "finance-001",
        "metadata": {
            "department": "Finance",
            "access_level": "manager",
            "allowed_roles": ["manager"],
        },
    }

    policy = AccessPolicy()

    assert not policy.can_access(
        user,
        document,
    )


def test_finance_manager_can_access_finance_document():

    user = UserContext(
        user_id="manager-001",
        role="manager",
        department="Finance",
    )

    document = {
        "id": "finance-001",
        "metadata": {
            "department": "Finance",
            "access_level": "manager",
            "allowed_roles": ["manager"],
        },
    }

    policy = AccessPolicy()

    assert policy.can_access(
        user,
        document,
    )


def test_finance_manager_cannot_access_hr_document():

    user = UserContext(
        user_id="manager-001",
        role="manager",
        department="Finance",
    )

    document = {
        "id": "hr-001",
        "metadata": {
            "department": "HR",
            "access_level": "employee",
            "allowed_roles": [
                "employee",
                "manager",
            ],
        },
    }

    policy = AccessPolicy()

    assert not policy.can_access(
        user,
        document,
    )


def test_wrong_role_blocks_document():

    user = UserContext(
        user_id="employee-001",
        role="employee",
        department="HR",
    )

    document = {
        "id": "finance-001",
        "metadata": {
            "department": "HR",
            "access_level": "employee",
            "allowed_roles": ["manager"],
        },
    }

    policy = AccessPolicy()

    assert not policy.can_access(
        user,
        document,
    )