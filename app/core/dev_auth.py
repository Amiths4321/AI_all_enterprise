from app.core.auth import Authenticator, Identity


class DevelopmentAuthenticator(Authenticator):

    USERS = {
        "employee-token": Identity(
            user_id="employee-001",
            role="employee",
            department="HR",
        ),
        "manager-token": Identity(
            user_id="manager-001",
            role="manager",
            department="Finance",
        ),
        "engineering-token": Identity(
            user_id="engineer-001",
            role="employee",
            department="Engineering",
        ),
    }

    def authenticate(self, token: str) -> Identity:
        identity = self.USERS.get(token)

        if identity is None:
            raise ValueError("Invalid authentication token")

        return identity