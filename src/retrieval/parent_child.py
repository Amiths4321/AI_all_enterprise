from dataclasses import dataclass
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class ParentChunk:
    id: str
    text: str
    metadata: dict[str, Any]


@dataclass
class ChildChunk:
    id: str
    parent_id: str
    text: str
    metadata: dict[str, Any]


def create_parent_child_chunks(
    documents,
    parent_size: int = 2000,
    parent_overlap: int = 200,
    child_size: int = 300,
    child_overlap: int = 50,
):
    """
    Split documents into larger parent chunks and
    smaller child chunks.

    Children are used for vector retrieval.
    Parents are used as LLM context.
    """

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=parent_size,
        chunk_overlap=parent_overlap,
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=child_size,
        chunk_overlap=child_overlap,
    )

    parents = []
    children = []

    parent_documents = parent_splitter.split_documents(documents)

    for parent_index, parent_doc in enumerate(parent_documents):

        parent_id = f"parent_{parent_index}"

        parent = ParentChunk(
            id=parent_id,
            text=parent_doc.page_content,
            metadata={
                **parent_doc.metadata,
                "parent_id": parent_id,
            },
        )

        parents.append(parent)

        child_documents = child_splitter.split_documents(
            [parent_doc]
        )

        for child_index, child_doc in enumerate(child_documents):

            child_id = (
                f"child_{parent_index}_{child_index}"
            )

            child = ChildChunk(
                id=child_id,
                parent_id=parent_id,
                text=child_doc.page_content,
                metadata={
                    **child_doc.metadata,
                    "parent_id": parent_id,
                    "child_id": child_id,
                },
            )

            children.append(child)

    return parents, children