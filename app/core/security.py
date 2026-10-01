from dataclasses import dataclass


ACCESS_RANK = {
    "employee": 1,
    "manager": 2,
}


@dataclass(frozen=True)
class UserContext:
    user_id: str
    role: str
    department: str


class AccessPolicy:

    def allowed_levels(self, user: UserContext) -> list[str]:
        user_rank = ACCESS_RANK.get(user.role, 0)

        return [
            level
            for level, rank in ACCESS_RANK.items()
            if rank <= user_rank
        ]

    def can_access(
        self,
        user: UserContext,
        document: dict,
    ) -> bool:

        metadata = document.get("metadata", {})

        required_level = metadata.get(
            "access_level",
            "employee",
        )

        if required_level not in self.allowed_levels(user):
            return False

        document_department = metadata.get("department")

        if (
            document_department is not None
            and document_department != user.department
        ):
            return False

        allowed_roles = metadata.get("allowed_roles")

        if (
            allowed_roles is not None
            and user.role not in allowed_roles
        ):
            return False

        return True