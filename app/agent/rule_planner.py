from app.agent.planner import Planner


class RuleBasedPlanner(Planner):

    COMPARISON_WORDS = {
        "compare",
        "difference",
        "versus",
        "vs",
    }

    def plan(
        self,
        question: str,
    ) -> list[str]:

        normalized = question.lower()

        if any(
            word in normalized
            for word in self.COMPARISON_WORDS
        ):
            parts = [
                part.strip()
                for part in question
                .replace(" vs ", "|")
                .replace(" versus ", "|")
                .split("|")
                if part.strip()
            ]

            if len(parts) >= 2:
                return parts

        if " and " in normalized:
            parts = [
                part.strip()
                for part in question.split(
                    " and "
                )
                if part.strip()
            ]

            if len(parts) == 2:
                return parts

        return [question]