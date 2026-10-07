import pytest

from app.core.config import (
    AppConfig,
    validate_config,
)


def test_valid_config():

    config = AppConfig(
        environment="test",
        ollama_url="http://localhost:11434",
        ollama_model="test-model",
        chroma_path="chroma_db",
        chroma_collection="documents",
        retrieval_top_k=10,
        reranking_top_n=3,
        request_timeout_seconds=120,
    )

    validate_config(config)


def test_invalid_top_n():

    config = AppConfig(
        environment="test",
        ollama_url="http://localhost:11434",
        ollama_model="test-model",
        chroma_path="chroma_db",
        chroma_collection="documents",
        retrieval_top_k=3,
        reranking_top_n=10,
        request_timeout_seconds=120,
    )

    with pytest.raises(ValueError):
        validate_config(config)