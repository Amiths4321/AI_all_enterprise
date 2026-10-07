from langchain_ollama import ChatOllama


class RepresentationGenerator:

    def __init__(
        self,
        model="qwen2.5vl",
    ):

        self.llm = ChatOllama(
            model=model,
            base_url="http://localhost:11434",
            temperature=0,
        )

    def generate_questions(
        self,
        text,
        count=3,
    ):

        prompt = f"""
Generate {count} questions that can be answered
using ONLY the following document passage.

Passage:
{text}

Return exactly {count} questions,
one per line.

Do not number them.
"""

        response = self.llm.invoke(prompt)

        questions = [
            line.strip()
            for line in response.content.splitlines()
            if line.strip()
        ]

        return questions[:count]