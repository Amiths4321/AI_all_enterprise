class ContextCompressor:

    def __init__(self, llm):
        self.llm = llm

    def compress(self, query, context):

        prompt = f"""
Extract ONLY the passages from the context that
directly help answer the question.

Do not add information.

Question:
{query}

Context:
{context}

Return only the relevant passages.
"""

        response = self.llm.invoke(prompt)

        return response.content