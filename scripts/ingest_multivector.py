import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

from src.retrieval.parent_child import create_parent_child_chunks
from src.retrieval.multivector.generator import RepresentationGenerator
from src.retrieval.multivector.store import MultiVectorStore


load_dotenv(override=True)

PDF_PATH = "data/document.pdf"


def main():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    parents, _ = create_parent_child_chunks(documents)

    generator = RepresentationGenerator()
    store = MultiVectorStore()

    existing_ids = set(
        store.vectorstore.get(include=[]).get("ids", [])
    )

    print(f"Parents: {len(parents)}")
    print(f"Existing vectors: {len(existing_ids)}")

    for index, parent in enumerate(parents):
        questions = generator.generate_questions(
            parent.text,
            count=3,
        )

        texts = []
        metadatas = []
        ids = []

        for i, question in enumerate(questions):
            vector_id = f"{parent.id}_question_{i}"

            if vector_id in existing_ids:
                continue

            texts.append(question)
            metadatas.append({
                "parent_id": parent.id,
                "representation": "hypothetical_question",
            })
            ids.append(vector_id)

        if texts:
            store.add_vectors(
                texts=texts,
                metadatas=metadatas,
                ids=ids,
            )

        print(
            f"[{index + 1}/{len(parents)}] "
            f"{parent.id} -> {len(texts)} new vectors"
        )

    print("\nMULTI-VECTOR INGESTION COMPLETE")


if __name__ == "__main__":
    main()