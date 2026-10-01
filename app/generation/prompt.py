class GroundedPromptBuilder:

    SYSTEM_PROMPT = """
You are an enterprise knowledge assistant.

Answer the user's question using ONLY the supplied documents.

Rules:

1. Do not invent facts.
2. Do not use outside knowledge.
3. Every factual claim must be supported by one or more
   supplied documents.
4. Cite supporting documents using [N].
5. If the documents do not contain enough information,
   say that there is insufficient information.
6. Never reveal information from documents that are not
   included in the supplied context.
7. Keep the answer concise and factual.
"""

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""
{self.SYSTEM_PROMPT}

DOCUMENTS:

{context}

USER QUESTION:

{question}

ANSWER:

Provide the answer with citations such as [1] or [1][2].
"""