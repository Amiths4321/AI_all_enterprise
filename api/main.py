from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3
from src.rag.multivector_pipeline import MultiVectorRAG
from src.rag.unified_pipeline import UnifiedRAG

from src.rag.pipeline import ParentChildRAG
from src.rag.memory import ChatMemory
import time


unified_rag = UnifiedRAG()

app = FastAPI(
    title="Enterprise RAG API",
    version="1.0.0",
)

# Load RAG once when the API starts
rag = ParentChildRAG()

# Persistent conversation memory
memory = ChatMemory()
multivector_rag = MultiVectorRAG()

class QueryRequest(BaseModel):
    question: str

# 1. Readiness / Health check endpoint
@app.get("/ready")
async def ready():
    return {"status": "ready"}

# 2. Main Query endpoint
@app.post("/query")
async def query_endpoint(request: QueryRequest):
    if not request.question:
        raise HTTPException(status_code=422, detail="Question cannot be empty")
    
    # Process query through RAG pipeline here
    return {
        "answer": "Processed query successfully",
        "sources": []
    }
    
class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=1000,
    )
    k: int = Field(
        default=5,
        ge=1,
        le=20,
    )
    expand: bool = False


# --------------------------------------------------
# Request model
# --------------------------------------------------

class ChatRequest(BaseModel):
    session_id: str = Field(
        min_length=1,
        max_length=100,
    )
    question: str = Field(
        min_length=1,
        max_length=2000,
    )
    mode: str = Field(
        default="multivector",
    )
    expand: bool = True


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "vector_database": "connected",
        "llm": "ollama",
        "embedding_model": "nomic-embed-text",
        "generation_model": "qwen2.5vl",
    }


# --------------------------------------------------
# Chat endpoint
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    if request.mode not in {
        "parent_child",
        "multivector",
    }:
        raise HTTPException(
            status_code=400,
            detail=(
                "mode must be "
                "'parent_child' or "
                "'multivector'"
            ),
        )

    try:
        history = memory.get_history(
            request.session_id
        )

        result = unified_rag.ask(
            request.question,
            mode=request.mode,
            expand=request.expand,
            history=history,
        )

        memory.add_message(
            request.session_id,
            "user",
            request.question,
        )

        memory.add_message(
            request.session_id,
            "assistant",
            result["answer"],
        )

        return {
            "question": result["query"],
            "answer": result["answer"],
            "mode": result["mode"],
            "sources": result["sources"],
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="RAG request failed.",
        )

@app.post("/compare")
def compare(request: SearchRequest):
    try:
        start = time.perf_counter()

        parent_child_start = time.perf_counter()

        parent_child_result = unified_rag.ask(
            request.query,
            mode="parent_child",
            expand=False,
        )

        parent_child_time = (
            time.perf_counter()
            - parent_child_start
        )

        multivector_start = time.perf_counter()

        multivector_result = unified_rag.ask(
            request.query,
            mode="multivector",
            expand=request.expand,
        )

        multivector_time = (
            time.perf_counter()
            - multivector_start
        )

        total_time = (
            time.perf_counter() - start
        )

        return {
            "query": request.query,
            "latency": {
                "parent_child_seconds": round(
                    parent_child_time,
                    3,
                ),
                "multivector_seconds": round(
                    multivector_time,
                    3,
                ),
                "total_seconds": round(
                    total_time,
                    3,
                ),
            },
            "parent_child": {
                "answer": parent_child_result[
                    "answer"
                ],
                "sources": parent_child_result[
                    "sources"
                ],
            },
            "multivector": {
                "answer": multivector_result[
                    "answer"
                ],
                "sources": multivector_result[
                    "sources"
                ],
            },
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Comparison failed.",
        )
# --------------------------------------------------
# Browser UI
# --------------------------------------------------
@app.post("/search")
def search_post(request: SearchRequest):
    try:
        results = multivector_rag.retrieve(
            request.query,
            k=request.k,
            expand=request.expand,
        )

        parents = multivector_rag.aggregate_parents(
            results
        )

        reranked = multivector_rag.rerank(
            request.query,
            parents,
            top_k=min(5, len(parents)),
        )

        return {
            "query": request.query,
            "expanded": request.expand,
            "results": [
                {
                    "parent_id": item["parent_id"],
                    "score": item["score"],
                    "reranker_score": item[
                        "reranker_score"
                    ],
                    "text": item["text"],
                }
                for item in reranked
            ],
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Search failed.",
        )

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)
@app.get("/health")
def health():
    try:
        vector_count = (
            multivector_rag
            .store
            .vectorstore
            ._collection
            .count()
        )

        return {
            "status": "ok",
            "parent_child": {
                "status": "ready",
            },
            "multivector": {
                "status": "ready",
                "vectors": vector_count,
            },
        }

    except Exception as exc:
        return {
            "status": "degraded",
            "error": str(exc),
        }

@app.get("/ui")
def ui():
    return FileResponse(
        "static/index.html"
    )
@app.delete("/chat/{session_id}")
def clear_session(session_id: str):
    # Add your logic to clear history for this session
    return {"status": "success", "message": f"Cleared session {session_id}"}

@app.get("/diagnostics")
def diagnostics():
    import json
    import os
    import statistics

    log_path = "logs/retrieval.jsonl"

    if not os.path.exists(log_path):
        return {
            "status": "ok",
            "records": 0,
            "message": "No retrieval requests logged yet.",
        }

    records = []

    with open(
        log_path,
        "r",
        encoding="utf-8",
    ) as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not records:
        return {
            "status": "ok",
            "records": 0,
            "message": "No valid retrieval records found.",
        }

    by_mode = {}

    for record in records:
        mode = record.get("mode", "unknown")

        by_mode.setdefault(mode, []).append(record)

    mode_stats = {}

    for mode, items in by_mode.items():
        latencies = [
            float(item["elapsed_seconds"])
            for item in items
            if "elapsed_seconds" in item
        ]

        stats = {
            "requests": len(items),
        }

        if latencies:
            stats.update(
                {
                    "average_latency_seconds": round(
                        statistics.mean(latencies),
                        4,
                    ),
                    "min_latency_seconds": round(
                        min(latencies),
                        4,
                    ),
                    "max_latency_seconds": round(
                        max(latencies),
                        4,
                    ),
                }
            )

        timing_names = [
            "retrieval",
            "aggregation",
            "rerank",
            "generation",
        ]

        for timing_name in timing_names:
            values = []

            for item in items:
                timings = item.get(
                    "timings",
                    {},
                )

                if timing_name in timings:
                    values.append(
                        float(
                            timings[timing_name]
                        )
                    )

            if values:
                stats[
                    f"average_{timing_name}_seconds"
                ] = round(
                    statistics.mean(values),
                    4,
                )

        mode_stats[mode] = stats

    return {
        "status": "ok",
        "records": len(records),
        "modes": mode_stats,
        "latest": records[-1],
    }
@app.delete("/chat/{session_id: str}")
def delete_chat(session_id: str):

    try:

        with sqlite3.connect(
            memory.db_path
        ) as conn:

            conn.execute(
                """
                DELETE FROM messages
                WHERE session_id = ?
                """,
                (session_id,),
            )

            conn.commit()

        return {
            "status": "deleted",
            "session_id": session_id,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not delete chat.",
        )

class SearchRequest(BaseModel):
    question: str

@app.post("/search")
def search(request: SearchRequest):

    try:

        query = request.question.strip()

        if not query:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )

        children = rag.retrieve(
            query,
            k=20,
        )

        parents = rag.score_parents(
            children
        )

        reranked = rag.rerank_parents(
            query,
            parents,
            top_k=5,
        )

        return {
            "query": query,
            "results": reranked,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Search failed.",
        )