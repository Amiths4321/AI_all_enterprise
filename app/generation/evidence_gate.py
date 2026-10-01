class EvidenceSufficiencyGate:

    def check(
        self,
        documents: list[dict],
    ) -> dict:

        if not documents:
            return {
                "sufficient": False,
                "reason": "no_authorized_evidence",
            }

        return {
            "sufficient": True,
            "reason": "authorized_evidence_available",
        }