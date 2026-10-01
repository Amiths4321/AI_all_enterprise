from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    required_evidence: list[str] = Field(default_factory=list)
    top_k: int = Field(default=10, ge=1, le=50)
    top_n: int = Field(default=3, ge=1, le=20)


class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved_documents: list[dict]
    reranked_documents: list[dict]
    evidence: dict