import re

from app.query.models import QueryEntity


class EntityExtractor:

    DEPARTMENTS = {
        "hr": "HR",
        "finance": "Finance",
        "engineering": "Engineering",
    }

    def extract(self, question: str) -> list[QueryEntity]:

        text = question.lower()
        entities = []

        for key, value in self.DEPARTMENTS.items():
            if key in text:
                entities.append(
                    QueryEntity(
                        name=value,
                        entity_type="department",
                    )
                )

        years = re.findall(r"\b20\d{2}\b", question)

        for year in years:
            entities.append(
                QueryEntity(
                    name=year,
                    entity_type="year",
                )
            )

        return entities