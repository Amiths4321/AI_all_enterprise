import pytest

from app.core.security import (
    AccessPolicy,
    UserContext,
)


@pytest.mark.parametrize(
    "user,document_id,expected",
    [
        (
            UserContext(
                "employee-001",
                "employee",
                "HR",
            ),
            "hr-001",
            True,
        ),
        (
            UserContext(
                "employee-001",
                "employee",
                "HR",
            ),
            "hr-002",
            True,
        ),
        (
            UserContext(
                "employee-001",
                "employee",
                "HR",
            ),
            "finance-001",
            False,
        ),
        (
            UserContext(
                "employee-001",
                "employee",
                "HR",
            ),
            "engineering-001",
            False,
        ),
        (
            UserContext(
                "manager-001",
                "manager",
                "Finance",
            ),
            "finance-001",
            True,
        ),
        (
            UserContext(
                "manager-001",
                "manager",
                "Finance",
            ),
            "hr-001",
            False,
        ),
        (
            UserContext(
                "manager-001",
                "manager",
                "Finance",
            ),
            "engineering-001",
            False,
        ),
        (
            UserContext(
                "engineering-token",
                "employee",
                "Engineering",
            ),
            "engineering-001",
            True,
        ),
        (
            UserContext(
                "engineering-token",
                "employee",
                "Engineering",
            ),
            "hr-001",
            False,
        ),
    ],
)
def test_document_authorization(
    user,
    document_id,
    expected,
):

    documents = {
        "hr-001": {
            "metadata": {
                "department": "HR",
                "access_level": "employee",
                "allowed_roles": [
                    "employee",
                    "manager",
                ],
            }
        },
        "hr-002": {
            "metadata": {
                "department": "HR",
                "access_level": "employee",
                "allowed_roles": [
                    "employee",
                    "manager",
                ],
            }
        },
        "finance-001": {
            "metadata": {
                "department": "Finance",
                "access_level": "manager",
                "allowed_roles": [
                    "manager",
                ],
            }
        },
        "engineering-001": {
            "metadata": {
                "department": "Engineering",
                "access_level": "employee",
                "allowed_roles": [
                    "employee",
                    "manager",
                ],
            }
        },
    }

    policy = AccessPolicy()

    assert (
        policy.can_access(
            user,
            documents[document_id],
        )
        == expected
    )