import json
import os
from collections import defaultdict

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

load_dotenv(override=True)

CHROMA_PATH = "chroma_db"
PARENT_STORE_PATH = "parent_store.json"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")


def load_parent_store():
    with open(PARENT_STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("Loading embedding model...")

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url="http://localhost:11434",
    )

    print("Loading Chroma...")

    vectorstore = Chroma(
        collection_name="enterprise_rag",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH,
    )

    print("Loading parent store...")

    parent_store = load_parent_store()

    print(f"Loaded {len(parent_store)} parents.")

    query = input("\nQuestion: ").strip()

    if not query:
        print("No question provided.")
        return

    # Retrieve more children so a parent can have multiple relevant matches.
    print("\nSearching child chunks...")

    results = vectorstore.similarity_search_with_score(
        query,
        k=20,
    )

    # ---------------------------------------------------------
    # Group child distances by parent
    # ---------------------------------------------------------

    parent_matches = defaultdict(list)

    for doc, distance in results:
        parent_id = doc.metadata.get("parent_id")

        if parent_id:
            parent_matches[parent_id].append(distance)

    # ---------------------------------------------------------
    # Calculate parent scores
    #
    # Chroma distance:
    # LOWER = MORE SIMILAR
    #
    # We use the average of the best 2 child distances.
    # ---------------------------------------------------------

    ranked_parents = []

    for parent_id, distances in parent_matches.items():

        distances.sort()

        best_distances = distances[:2]

        parent_score = sum(best_distances) / len(best_distances)

        ranked_parents.append(
            {
                "parent_id": parent_id,
                "score": parent_score,
                "children_hit": len(distances),
                "best_child_distance": distances[0],
            }
        )

    # Lower distance = better parent match
    ranked_parents.sort(key=lambda x: x["score"])

    # ---------------------------------------------------------
    # Display child retrieval
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("TOP CHILD RETRIEVAL")
    print("=" * 80)

    for rank, (doc, distance) in enumerate(results, start=1):

        print(f"\nRank              : {rank}")
        print(f"Child distance    : {distance}")
        print(f"Child ID          : {doc.metadata.get('child_id')}")
        print(f"Parent ID         : {doc.metadata.get('parent_id')}")

        print("\nChild text:")
        print(doc.page_content[:500])

    # ---------------------------------------------------------
    # Display parent ranking
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("PARENT-LEVEL RANKING")
    print("=" * 80)

    for rank, item in enumerate(ranked_parents[:10], start=1):

        parent_id = item["parent_id"]
        parent = parent_store.get(parent_id)

        print(f"\nParent Rank       : {rank}")
        print(f"Parent ID         : {parent_id}")
        print(f"Parent Score      : {item['score']}")
        print(f"Best Child Dist.  : {item['best_child_distance']}")
        print(f"Children Hit      : {item['children_hit']}")

        if parent:
            print("\nParent text:")
            print(parent["text"][:1500])


if __name__ == "__main__":
    main()