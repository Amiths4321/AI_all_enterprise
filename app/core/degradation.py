class DegradationPolicy:

    def no_generation_available(self):

        return {
            "answer": (
                "The answer service is "
                "temporarily unavailable."
            ),
            "grounded": False,
            "degraded": True,
        }

    def no_evidence(self):

        return {
            "answer": (
                "I don't have enough "
                "authorized information "
                "to answer that question."
            ),
            "grounded": False,
            "degraded": False,
        }