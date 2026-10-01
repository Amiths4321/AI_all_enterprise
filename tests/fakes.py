class FakeRetriever:

    def retrieve(
        self,
        question,
        top_k=10,
    ):
        return [
            {
                "id": "test-1",
                "document": "Annual leave is 20 days.",
                "metadata": {
                    "source": "hr_policy.txt"
                },
                "score": 1.0,
            }
        ]


class FakeReranker:

    def rerank(
        self,
        question,
        documents,
        top_n=3,
    ):
        return documents[:top_n]


class FakeEvidenceEvaluator:

    def evaluate(
        self,
        required_evidence,
        retrieved_documents,
    ):
        return {
            "evidence_recall": 1.0,
            "matches": [],
        }


class FakeGenerator:

    def generate(
        self,
        question,
        documents,
    ):
        return "TEST ANSWER"