import json
import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from src.retrieval.parent_child import (
    create_parent_child_chunks,
)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv(override=True)

os.environ["OLLAMA_HOST"] = "http://localhost:11434"

PDF_PATH = "data/document.pdf"
CHROMA_PATH = "chroma_db"
PARENT_STORE_PATH = "parent_store.json"

EMBEDDING_MODEL = "nomic-embed-text"

# Keep this small because your machine is running
# the embedding model on CPU.
BATCH_SIZE = 10


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    # ----------------------------------------------
    # 1. Load document
    # ----------------------------------------------

    print("Loading document...")

    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages.")


    # ----------------------------------------------
    # 2. Create parent-child chunks
    # ----------------------------------------------

    print("Creating parent-child chunks...")

    parents, children = create_parent_child_chunks(
        documents
    )

    print(f"Parents: {len(parents)}")
    print(f"Children: {len(children)}")


    # ----------------------------------------------
    # 3. Save parent chunks
    # ----------------------------------------------

    print("Saving parent chunks...")

    parent_store = {
        parent.id: {
            "text": parent.text,
            "metadata": parent.metadata,
        }
        for parent in parents
    }

    with open(
        PARENT_STORE_PATH,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            parent_store,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print("Parent store saved.")


    # ----------------------------------------------
    # 4. Create embedding model
    # ----------------------------------------------

    print(
        f"Loading embedding model: "
        f"{EMBEDDING_MODEL}"
    )

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url="http://localhost:11434",
    )


    # ----------------------------------------------
    # 5. Create Chroma collection
    # ----------------------------------------------

    print("Creating Chroma database...")

    vectorstore = Chroma(
        collection_name="enterprise_rag",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH,
    )


    # ----------------------------------------------
    # 6. Embed children in batches
    # ----------------------------------------------

    print("Starting child embedding...")

    total_children = len(children)

    for start in range(
        0,
        total_children,
        BATCH_SIZE,
    ):

        batch = children[
            start:start + BATCH_SIZE
        ]

        end = start + len(batch)

        print(
            f"Embedding children "
            f"{start + 1}-{end} "
            f"of {total_children}"
        )

        vectorstore.add_texts(

            texts=[
                child.text
                for child in batch
            ],

            metadatas=[
                child.metadata
                for child in batch
            ],

            ids=[
                child.id
                for child in batch
            ],
        )


    # ----------------------------------------------
    # 7. Finished
    # ----------------------------------------------

    print()
    print("=" * 50)
    print("INGESTION COMPLETE")
    print("=" * 50)

    print(f"Parents: {len(parents)}")
    print(f"Children indexed: {total_children}")

    print("=" * 50)


if __name__ == "__main__":
    main()