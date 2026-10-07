from collections import defaultdict
import time

from langchain_ollama import ChatOllama

from src.retrieval.multivector.store import MultiVectorStore
from src.retrieval.multivector.query_expander import QueryExpander
from src.retrieval.reranker import LocalReranker
from src.rag.retrieval_logger import RetrievalLogger


class MultiVectorRAG:
    def __init__(self, llm_model="qwen2.5vl"):
        self.store = MultiVectorStore()
        self.reranker = LocalReranker()
        self.query_expander = QueryExpander(model=llm_model)
        self.llm = ChatOllama(
            model=llm_model,
            base_url="http://localhost:11434",
            temperature=0,
        )
        self.logger = RetrievalLogger()

    def retrieve(self, query, k=12, expand=True):
        if expand:
            queries = self.query_expander.expand(query, count=3)
        else:
            queries = [query]

        all_results = []
        seen = set()

        for expanded_query in queries:
            results = self.store.search(expanded_query, k=k)

            for doc, distance in results:
                parent_id = doc.metadata.get("parent_id")

                representation_type = doc.metadata.get(
                    "representation",
                    "unknown",
                )

                representation = doc.page_content

                result_id = (
                    f"{parent_id}|"
                    f"{representation_type}|"
                    f"{representation}"
                )

                if result_id in seen:
                    continue

                seen.add(result_id)

                all_results.append(
                    {
                        "doc": doc,
                        "distance": float(distance),
                        "parent_id": parent_id,
                        "representation_type": representation_type,
                        "representation": representation,
                    }
                )

        all_results.sort(key=lambda item: item["distance"])

        return all_results

    def aggregate_parents(self, results):
        grouped = defaultdict(list)

        for result in results:
            parent_id = result["parent_id"]

            if not parent_id:
                continue

            grouped[parent_id].append(
                {
                    "distance": result["distance"],
                    "representation": result["representation"],
                    "type": result["representation_type"],
                }
            )

        ranked = []

        for parent_id, matches in grouped.items():
            matches.sort(key=lambda item: item["distance"])

            best = matches[:3]

            score = sum(
                item["distance"] for item in best
            ) / len(best)

            parent = self.store.get_parent(parent_id)

            if not parent:
                continue

            ranked.append(
                {
                    "parent_id": parent_id,
                    "score": score,
                    "matches": best,
                    "text": parent["text"],
                }
            )

        ranked.sort(key=lambda item: item["score"])

        return ranked

    def rerank(self, query, parents, top_k=3):
        if not parents:
            return []

        candidates = parents[:10]

        documents = [
            item["text"]
            for item in candidates
        ]

        reranked = self.reranker.rerank(
            query,
            documents,
            top_k=min(top_k, len(documents)),
        )

        final = []

        for text, reranker_score in reranked:
            for candidate_index, item in enumerate(candidates):
                if item["text"] == text:
                    final.append(
                        {
                            **item,
                            "candidate_index": candidate_index,
                            "reranker_score": float(
                                reranker_score
                            ),
                        }
                    )
                    break

        return final

    def build_context(self, results):
        parts = []

        for rank, item in enumerate(results, start=1):
            parts.append(
                f"[Source {rank} | Parent: {item['parent_id']}]\n"
                f"{item['text']}"
            )

        return "\n\n".join(parts)

    def generate(self, query, context):
        if not context.strip():
            return (
                "I do not have enough information in the "
                "retrieved documents to answer that."
            )

        prompt = f"""
You are an enterprise document question-answering assistant.

Answer ONLY using the retrieved context.

Rules:
1. Do not invent facts.
2. Every factual claim must have a citation like [Source 1].
3. Use only the source numbers provided in the context.
4. If the context is insufficient, say:
   "I do not have enough information in the retrieved documents to answer that."
5. Keep the answer concise.

Question:
{query}

Retrieved context:
{context}

Answer:
"""

        response = self.llm.invoke(prompt)
        answer = response.content.strip()

        if not answer:
            return (
                "I do not have enough information in the "
                "retrieved documents to answer that."
            )

        return answer

    def ask(self, query, expand=True):
        start = time.perf_counter()

        t0 = time.perf_counter()
        retrieved = self.retrieve(query, k=8, expand=expand)
        retrieval_seconds = time.perf_counter() - t0

        t0 = time.perf_counter()
        parents = self.aggregate_parents(retrieved)
        aggregation_seconds = time.perf_counter() - t0

        t0 = time.perf_counter()
        reranked = self.rerank(query, parents, top_k=3)
        rerank_seconds = time.perf_counter() - t0

        context = self.build_context(reranked)

        t0 = time.perf_counter()
        answer = self.generate(query, context)
        generation_seconds = time.perf_counter() - t0

        elapsed = time.perf_counter() - start

        log_results = []

        for item in reranked:
            log_results.append(
                {
                    "parent_id": item["parent_id"],
                    "score": item["score"],
                    "reranker_score": item["reranker_score"],
                }
            )

        self.logger.log(
            query=query,
            results=log_results,
            elapsed_seconds=elapsed,
            mode=(
                "multivector_expanded"
                if expand
                else "multivector"
            ),
            timings={
                "retrieval": retrieval_seconds,
                "aggregation": aggregation_seconds,
                "rerank": rerank_seconds,
                "generation": generation_seconds,
            },
            metadata={
                "retrieved_vectors": len(retrieved),
                "candidate_parents": len(parents),
                "final_sources": len(reranked),
            },
        )

        return {
            "query": query,
            "answer": answer,
            "sources": reranked,
            "elapsed_seconds": elapsed,
            "timings": {
                "retrieval": retrieval_seconds,
                "aggregation": aggregation_seconds,
                "rerank": rerank_seconds,
                "generation": generation_seconds,
            },
        }