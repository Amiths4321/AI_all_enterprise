from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:

    environment: str
    ollama_url: str
    ollama_model: str

    chroma_path: str
    chroma_collection: str

    retrieval_top_k: int
    reranking_top_n: int

    request_timeout_seconds: int


def load_config() -> AppConfig:

    return AppConfig(
        environment=os.getenv(
            "APP_ENV",
            "development",
        ),
        ollama_url=os.getenv(
            "OLLAMA_URL",
            "http://10.22.39.192:11434",
        ),
        ollama_model=os.getenv(
            "OLLAMA_MODEL",
            "qwen2.5vl:latest",
        ),
        chroma_path=os.getenv(
            "CHROMA_PATH",
            "chroma_db",
        ),
        chroma_collection=os.getenv(
            "CHROMA_COLLECTION",
            "enterprise_documents",
        ),
        retrieval_top_k=int(
            os.getenv(
                "RETRIEVAL_TOP_K",
                "10",
            )
        ),
        reranking_top_n=int(
            os.getenv(
                "RERANKING_TOP_N",
                "3",
            )
        ),
        request_timeout_seconds=int(
            os.getenv(
                "REQUEST_TIMEOUT_SECONDS",
            "120",
            )
        ),
    )

def validate_config(
    config: AppConfig,
):

    if not config.ollama_url:
        raise ValueError(
            "OLLAMA_URL is required"
        )

    if not config.ollama_model:
        raise ValueError(
            "OLLAMA_MODEL is required"
        )

    if config.retrieval_top_k <= 0:
        raise ValueError(
            "RETRIEVAL_TOP_K must be positive"
        )

    if config.reranking_top_n <= 0:
        raise ValueError(
            "RERANKING_TOP_N must be positive"
        )

    if (
        config.reranking_top_n
        > config.retrieval_top_k
    ):
        raise ValueError(
            "RERANKING_TOP_N cannot exceed "
            "RETRIEVAL_TOP_K"
        )

    if config.request_timeout_seconds <= 0:
        raise ValueError(
            "REQUEST_TIMEOUT_SECONDS must be positive"
        )

        