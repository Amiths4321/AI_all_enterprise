class GroundedGenerator:

    def __init__(
        self,
        generator,
        context_builder,
        context_renderer,
        prompt_builder,
    ):
        self.generator = generator
        self.context_builder = context_builder
        self.context_renderer = context_renderer
        self.prompt_builder = prompt_builder

    def generate(
        self,
        question: str,
        documents: list[dict],
    ):

        context_documents = (
            self.context_builder.build(documents)
        )

        context = self.context_renderer.render(
            context_documents
        )

        prompt = self.prompt_builder.build(
            question,
            context,
        )

        answer = self.generator.generate(
            prompt,
            [],
        )

        return {
            "answer": answer,
            "context_documents": context_documents,
            "prompt": prompt,
        }