import json
import os
from collections import defaultdict

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

load_dotenv(override=True)

CHROMA_PATH = "chroma_db"
PARENT_STORE_PATH = "parent_store.json"

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text",
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "qwen2.5vl",
)


def load_parent_store():
    with open(PARENT_STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def rerank_parents(query, ranked_parents, parent_store):
    reranked = []

    query_terms = set(
        word.lower()
        for word in query.split()
        if len(word) > 2
    )

    for item in ranked_parents:

        parent_id = item["parent_id"]
        parent = parent_store.get(parent_id)

        if not parent:
            continue

        text = parent["text"].lower()

        # Simple lexical overlap
        matching_terms = sum(
            1 for term in query_terms
            if term in text
        )

        reranked.append(
            {
                **item,
                "lexical_matches": matching_terms,
            }
        )

    # First use semantic parent score.
    # Lower semantic distance is better.
    #
    # Lexical overlap is only a secondary signal.
    reranked.sort(
        key=lambda x: (
            -x["lexical_matches"],
            x["score"],
        )
    )

    return reranked

def main():

    # -----------------------------
    # Load embedding model
    # -----------------------------

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url="http://localhost:11434",
    )

    # -----------------------------
    # Load vector database
    # -----------------------------

    vectorstore = Chroma(
        collection_name="enterprise_rag",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH,
    )

    # -----------------------------
    # Load parent documents
    # -----------------------------

    parent_store = load_parent_store()

    # -----------------------------
    # Load local LLM
    # -----------------------------

    llm = ChatOllama(
        model=LLM_MODEL,
        base_url="http://localhost:11434",
        temperature=0,
    )

    # -----------------------------
    # User question
    # -----------------------------

    query = input("\nQuestion: ").strip()

    if not query:
        return

    # -----------------------------
    # Retrieve child chunks
    # -----------------------------

    results = vectorstore.similarity_search_with_score(
        query,
        k=20,
    )

    # -----------------------------
    # Group children by parent
    # -----------------------------

    parent_matches = defaultdict(list)

    for doc, distance in results:

        parent_id = doc.metadata.get("parent_id")

        if parent_id:
            parent_matches[parent_id].append(distance)

    # -----------------------------
    # Score parents
    # -----------------------------

    ranked_parents = []

    for parent_id, distances in parent_matches.items():

        distances.sort()

        best_distances = distances[:2]

        score = sum(best_distances) / len(best_distances)

        ranked_parents.append(
            {
                "parent_id": parent_id,
                "score": score,
            }
        )

    ranked_parents.sort(
        key=lambda x: x["score"]
    )

    # -----------------------------
    # Select top parents
    # -----------------------------

    ranked_parents = rerank_parents(
        query,
        ranked_parents,
        parent_store,
    )

    top_parents = ranked_parents[:3]

    print("\n" + "=" * 80)
    print("FINAL PARENT SELECTION")
    print("=" * 80)

    for rank, item in enumerate(top_parents, start=1):
        print(
            f"{rank}. {item['parent_id']} | "
            f"semantic={item['score']:.4f} | "
            f"lexical={item['lexical_matches']}"
        )
    # -----------------------------
    # Build context
    # -----------------------------

    context_parts = []

    for item in top_parents:

        parent_id = item["parent_id"]

        parent = parent_store.get(parent_id)

        if not parent:
            continue

        context_parts.append(
            f"[Parent: {parent_id}]\n"
            f"{parent['text']}"
        )

    context = "\n\n".join(context_parts)

    # -----------------------------
    # Prompt
    # -----------------------------

    prompt = f"""
You are answering questions using retrieved document context.

Use ONLY the provided context.

If the context does not contain enough information
to answer the question, say that the information
is not available in the retrieved context.

Do not invent facts.

Question:
{query}

Retrieved context:
{context}

Answer:
"""

    # -----------------------------
    # Generate answer
    # -----------------------------

    print("\nGenerating answer...\n")

    response = llm.invoke(prompt)

    print("=" * 80)
    print("RAG ANSWER")
    print("=" * 80)

    print(response.content)


if __name__ == "__main__":
    main()