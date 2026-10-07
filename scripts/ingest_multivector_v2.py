import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

from src.retrieval.parent_child import create_parent_child_chunks
from src.retrieval.multivector.generator_v2 import (
    RepresentationGenerator,
)
from src.retrieval.multivector.store import (
    MultiVectorStore,
)


load_dotenv(override=True)

PDF_PATH = "data/document.pdf"


def main():
    loader = PyPDFLoader(PDF_PATH)

    documents = loader.load()

    parents, _ = create_parent_child_chunks(
        documents,
    )

    generator = RepresentationGenerator()
    store = MultiVectorStore()

    existing = store.existing_ids()

    print(f"Parents: {len(parents)}")
    print(f"Existing vectors: {len(existing)}")

    for index, parent in enumerate(parents, start=1):

        print(
            f"\n[{index}/{len(parents)}] "
            f"{parent.id}"
        )

        representations = []

        questions = generator.generate_questions(
            parent.text,
            count=3,
        )

        for i, question in enumerate(questions):
            representations.append(
                (
                    f"{parent.id}_question_{i}",
                    question,
                    "hypothetical_question",
                )
            )

        summary_id = f"{parent.id}_summary"

        summary = generator.generate_summary(
            parent.text,
        )

        representations.append(
            (
                summary_id,
                summary,
                "summary",
            )
        )

        texts = []
        metadatas = []
        ids = []

        for vector_id, text, representation_type in representations:

            if vector_id in existing:
                continue

            if not text.strip():
                continue

            ids.append(vector_id)
            texts.append(text)

            metadatas.append(
                {
                    "parent_id": parent.id,
                    "representation": representation_type,
                }
            )

        if texts:
            store.add_vectors(
                texts=texts,
                metadatas=metadatas,
                ids=ids,
            )

            existing.update(ids)

        print(
            f"Added {len(texts)} representations"
        )

    print("\n" + "=" * 80)
    print("MULTI-VECTOR V2 INGESTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
