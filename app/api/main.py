from pathlib import Path

from fastapi import FastAPI

from app.api.models import QueryRequest, QueryResponse
from app.core.application import Application


documents = [
    {
        "id": "hr-001",
        "document": (
            "Employees receive 20 days of annual leave "
            "per calendar year."
        ),
        "metadata": {
            "source": "hr_policy.txt",
        },
    },
    {
        "id": "hr-002",
        "document": (
            "Employees must submit annual leave requests "
            "through the HR portal."
        ),
        "metadata": {
            "source": "leave_process.txt",
        },
    },
    {
        "id": "benefits-001",
        "document": (
            "Employees receive health insurance coverage "
            "under the company benefits program."
        ),
        "metadata": {
            "source": "benefits.txt",
        },
    },
]


application = Application(
    documents=documents,
    config_path="configs/development.json",
)

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


@app.post(
    "/query",
    response_model=QueryResponse,
)
def query(request: QueryRequest):

    rag_service = application.get_rag_service()

    return rag_service.answer(
        question=request.question,
        required_evidence=request.required_evidence,
        top_k=request.top_k,
        top_n=request.top_n,
    )