from fastapi import FastAPI, HTTPException,Header

from app.api.models import QueryRequest, QueryResponse
from app.core.application import Application
from app.core.dev_auth import DevelopmentAuthenticator
from app.core.security import UserContext

application = Application(
    config_path="configs/development.json",
)
authenticator = DevelopmentAuthenticator()

application.startup()


app = FastAPI(
    title="Enterprise RAG",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.get("/ready")
def ready():

    if not application.is_ready():
        raise HTTPException(
            status_code=503,
            detail="Application is not ready.",
        )

    return {
        "status": "ready",
    }


@app.post("/query")
def query(
    request: QueryRequest,
    authorization: str | None = Header(default=None),
):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization token",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format",
        )

    token = authorization.removeprefix("Bearer ")

    try:
        identity = authenticator.authenticate(token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    user = UserContext(
        user_id=identity.user_id,
        role=identity.role,
        department=identity.department,
    )

    # pass user into the secure RAG service