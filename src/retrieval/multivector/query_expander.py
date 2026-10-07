
from langchain_ollama import ChatOllama


class QueryExpander:

    def __init__(
        self,
        model="qwen2.5vl",
    ):
        self.llm = ChatOllama(
            model=model,
            base_url="http://localhost:11434",
            temperature=0,
        )

    def expand(
        self,
        query,
        count=3,
    ):
        prompt = f"""
Generate {count} alternative search queries
for the following user question.

Preserve the original meaning.

Use different wording and terminology
that could improve document retrieval.

Question:
{query}

Return exactly {count} queries.
One per line.
Do not number them.
"""

        response = self.llm.invoke(prompt)

        queries = [
            line.strip()
            for line in response.content.splitlines()
            if line.strip()
        ]

        return [query] + queries[:count]
