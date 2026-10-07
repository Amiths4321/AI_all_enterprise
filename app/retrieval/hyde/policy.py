class HyDEPolicy:

    def should_use_hyde(
        self,
        question: str,
    ) -> bool:

        words = question.lower().split()

        if len(words) >= 12:
            return True

        semantic_indicators = [
            "explain",
            "why",
            "describe",
            "relationship",
            "how does",
        ]

        return any(
            indicator in question.lower()
            for indicator in semantic_indicators
        )
from app.retrieval.hyde.policy import HyDEPolicy


def test_hyde_policy():

    policy = HyDEPolicy()

    assert policy.should_use_hyde(
        "Explain how the leave process works."
    )

    assert not policy.should_use_hyde(
        "How many leave days?"
    )