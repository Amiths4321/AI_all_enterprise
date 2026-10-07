
from langchain_ollama import ChatOllama


class QueryRewriter:

    def __init__(
        self,
        model="qwen2.5vl",
    ):
        self.llm = ChatOllama(
            model=model,
            base_url="http://localhost:11434",
            temperature=0,
        )

    def rewrite(
        self,
        query,
        history=None,
    ):
        if not history:
            return query

        history_text = "\n".join(
            f"{role}: {content}"
            for role, content in history[-6:]
        )

        prompt = f"""
Rewrite the user's latest question into a
standalone search query.

Use the conversation history only to resolve
references such as:
- it
- this
- that
- they
- the book
- the document
- previous topics

Do not answer the question.

If the latest question is already standalone,
return it unchanged.

Conversation:
{history_text}

Latest question:
{query}

Standalone search query:
"""

        response = self.llm.invoke(prompt)

        rewritten = response.content.strip()

        return rewritten or query
