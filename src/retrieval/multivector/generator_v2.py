
from langchain_ollama import ChatOllama


class RepresentationGenerator:
    def __init__(self, model="qwen2.5vl"):
        self.llm = ChatOllama(
            model=model,
            base_url="http://localhost:11434",
            temperature=0,
        )

    def _invoke(self, prompt):
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def generate_questions(self, text, count=3):
        prompt = f"""
Generate {count} different questions that can be
answered using ONLY the document passage below.

The questions should cover different aspects of the passage.

Passage:
{text}

Return exactly {count} questions.
One question per line.
Do not number them.
"""

        content = self._invoke(prompt)

        questions = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        return questions[:count]

    def generate_summary(self, text):
        prompt = f"""
Create a concise factual summary of this document passage.

Preserve important:
- concepts
- terminology
- purposes
- relationships
- technical details

Do not introduce information not present in the passage.

Passage:
{text}

Summary:
"""

        return self._invoke(prompt)
