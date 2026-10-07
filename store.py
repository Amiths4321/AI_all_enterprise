import json
import os

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


class MultiVectorStore:

    def __init__(
        self,
        collection_name="enterprise_multivector",
        persist_directory="multivector_db",
        parent_store_path="parent_store.json",
    ):

        self.embeddings = OllamaEmbeddings(
            model=os.getenv(
                "EMBEDDING_MODEL",
                "nomic-embed-text",
            ),
            base_url="http://localhost:11434",
        )

        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory,
        )

        with open(
            parent_store_path,
            "r",
            encoding="utf-8",
        ) as f:
            self.parent_store = json.load(f)

    def add_vectors(
        self,
        texts,
        metadatas,
        ids,
    ):

        self.vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=ids,
        )

    def search(
        self,
        query,
        k=5,
    ):

        return self.vectorstore.similarity_search_with_score(
            query,
            k=k,
        )

    def get_parent(
        self,
        parent_id,
    ):

        return self.parent_store.get(
            parent_id
        )