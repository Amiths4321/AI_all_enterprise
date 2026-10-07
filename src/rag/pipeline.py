from collections import defaultdict
import json
from fastapi import HTTPException

from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

from src.rag.compressor import ContextCompressor
from src.retrieval.reranker import LocalReranker
from src.rag.monitoring import timed
from src.rag.cache import ResponseCache

class ParentChildRAG:

    def __init__(
        self,
        chroma_path="chroma_db",
        parent_store_path="parent_store.json",
        embedding_model="nomic-embed-text",
        llm_model="qwen2.5vl",
    ):

        print("Loading embeddings...")
        self.cache = ResponseCache()
        self.embeddings = OllamaEmbeddings(
            model=embedding_model,
            base_url="http://localhost:11434",
        )

        print("Loading Chroma...")

        self.vectorstore = Chroma(
            collection_name="enterprise_rag",
            embedding_function=self.embeddings,
            persist_directory=chroma_path,
        )

        print("Loading parent store...")

        with open(
            parent_store_path,
            "r",
            encoding="utf-8",
        ) as f:
            self.parent_store = json.load(f)

        print("Loading Qwen...")

        self.llm = ChatOllama(
            model=llm_model,
            base_url="http://localhost:11434",
            temperature=0,
        )

        print("Loading compressor...")
        # ✅ Initialized properly inside __init__ using self.llm
        self.compressor = ContextCompressor(self.llm)

        print("Loading reranker...")

        self.reranker = LocalReranker()

    # --------------------------------------------------
    # QUERY REWRITING
    # --------------------------------------------------

    def rewrite_query(
        self,
        query,
        chat_history=None,
    ):

        if not chat_history:
            return query

        history_text = "\n".join(
            f"{role}: {message}"
            for role, message in chat_history[-6:]
        )

        prompt = f"""
Rewrite the user's latest question into a standalone
question that can be understood without the conversation.

Conversation:
{history_text}

Latest question:
{query}

Return ONLY the rewritten question.
"""

        response = self.llm.invoke(prompt)

        return response.content.strip()

    # --------------------------------------------------
    # CHILD RETRIEVAL
    # --------------------------------------------------
    @timed("retrieval")
    def retrieve(
        self,
        query,
        k=20,
        metadata_filter=None,
    ):
        return self.vectorstore.similarity_search_with_score(
            query,
            k=k,
            filter=metadata_filter,
        )

    # --------------------------------------------------
    # PARENT AGGREGATION
    # --------------------------------------------------
    @timed("parent_scoring")
    def score_parents(self, results):

        parent_matches = defaultdict(list)

        for doc, distance in results:

            parent_id = doc.metadata.get(
                "parent_id"
            )

            if parent_id:
                parent_matches[parent_id].append(
                    distance
                )

        ranked = []

        for parent_id, distances in parent_matches.items():

            distances.sort()

            best = distances[:2]

            score = sum(best) / len(best)

            ranked.append(
                {
                    "parent_id": parent_id,
                    "score": score,
                    "children_hit": len(distances),
                }
            )

        ranked.sort(
            key=lambda item: item["score"]
        )

        return ranked

    # --------------------------------------------------
    # RERANK PARENTS
    # --------------------------------------------------
    @timed("reranking")
    def rerank_parents(
        self,
        query,
        ranked_parents,
        top_k=3,
    ):

        candidates = []

        for item in ranked_parents:

            parent_id = item["parent_id"]

            parent = self.parent_store.get(
                parent_id
            )

            if not parent:
                continue

            candidates.append(
                {
                    "parent_id": parent_id,
                    "text": parent["text"],
                    "retrieval_score": item["score"],
                    "children_hit": item[
                        "children_hit"
                    ],
                }
            )

        if not candidates:
            return []

        documents = [
            item["text"]
            for item in candidates
        ]

        reranked = self.reranker.rerank(
            query,
            documents,
            top_k=top_k,
        )

        final = []

        for text, reranker_score in reranked:

            match = next(
                item
                for item in candidates
                if item["text"] == text
            )

            final.append(
                {
                    **match,
                    "reranker_score": float(
                        reranker_score
                    ),
                }
            )

        return final

    # --------------------------------------------------
    # CONTEXT
    # --------------------------------------------------

    def build_context(
        self,
        ranked_parents,
    ):

        parts = []

        for rank, item in enumerate(
            ranked_parents,
            start=1,
        ):

            parts.append(
                f"[Source {rank} | "
                f"{item['parent_id']}]\n"
                f"{item['text']}"
            )

        return "\n\n".join(parts)

    # --------------------------------------------------
    # GENERATION
    # --------------------------------------------------
    @timed("generation")
    def generate(
        self,
        query,
        context,
    ):

        prompt = f"""
You are a document question-answering assistant.

Answer ONLY from the retrieved context.

Cite factual claims using [Source N].

Do not invent information.

If the answer is not supported by the context,
say:

"I don't have enough information in the retrieved
context to answer that."

Question:
{query}

Retrieved context:
{context}

Answer:
"""

        response = self.llm.invoke(prompt)

        return response.content

    # --------------------------------------------------
    # MAIN RAG FUNCTION
    # --------------------------------------------------
    def generate_query_variants(self, query):

        prompt = f"""
    Generate 3 alternative search queries for the
    following document question.

    Preserve the original meaning.

    Question:
    {query}

    Return exactly 3 queries, one per line.
    Do not number them.
    """

        response = self.llm.invoke(prompt)

        queries = [
            line.strip()
            for line in response.content.splitlines()
            if line.strip()
        ]

        return [query] + queries[:3]

    def multi_query_retrieve(self, query):

        queries = self.generate_query_variants(query)

        all_results = []

        for variant in queries:

            results = self.retrieve(
                variant,
                k=10,
            )

            all_results.extend(results)

        return all_results
    def has_sufficient_context(
        self,
        parents,
        minimum_reranker_score=0.0,
    ):
        if not parents:
            return False

        best_score = parents[0]["reranker_score"]

        return best_score >= minimum_reranker_score

    def ask(
        self,
        query,
        chat_history=None,
    ):
        cached = self.cache.get(query)

        if cached:
            return cached
        standalone_query = self.rewrite_query(
            query,
            chat_history,
        )

        # ✅ Fixed spacing typo here
        children = self.multi_query_retrieve(
            standalone_query
        )

        parents = self.score_parents(
            children
        )

        final_parents = self.rerank_parents(
            standalone_query,
            parents,
            top_k=3,
        )

        context = self.build_context(
            final_parents
        )

        context = self.compressor.compress(
            standalone_query,
            context,
        )

        answer = self.generate(
            standalone_query,
            context,
        )
        if not self.has_sufficient_context(
            final_parents,
            minimum_reranker_score=0.0,
        ):
            result = {
                "query": standalone_query,
                "answer": answer,
                "sources": final_parents,
            }

            self.cache.set(
                query,
                result,
            )

            return result