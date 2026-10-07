from app.retrieval.hyde.generator import (
    HypotheticalDocumentGenerator,
)


class FakeHyDEGenerator(
    HypotheticalDocumentGenerator
):

    def generate(self, question: str) -> str:
        return (
            "Employees receive annual leave according "
            "to the organization's leave policy."
        )


def test_hyde_generator_contract():

    generator = FakeHyDEGenerator()

    result = generator.generate(
        "How many annual leave days do employees receive?"
    )

    assert result
    assert "leave" in result.lower()