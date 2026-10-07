from app.query.dependency import QueryNode
from app.query.models import QueryPlan
from app.query.query_relationship import QueryRelationship
from app.query.relationship_classifier import (
    QueryRelationshipClassifier,
)


class QueryDependencyPlanner:

    def __init__(
        self,
        relationship_classifier=None,
    ):
        self.relationship_classifier = (
            relationship_classifier
            or QueryRelationshipClassifier()
        )

    def plan(
        self,
        query_plan: QueryPlan,
    ) -> list[QueryNode]:

        questions = query_plan.sub_questions

        if not questions:
            return []

        relationship = (
            self.relationship_classifier.classify(
                query_plan.original_question,
                questions,
            )
        )

        if relationship == QueryRelationship.DEPENDENT:

            nodes = [
                QueryNode(
                    query_id="q1",
                    question=questions[0],
                    depends_on=[],
                )
            ]

            for index, question in enumerate(
                questions[1:],
                start=2,
            ):
                nodes.append(
                    QueryNode(
                        query_id=f"q{index}",
                        question=question,
                        depends_on=["q1"],
                    )
                )

            return nodes

        return [
            QueryNode(
                query_id=f"q{index}",
                question=question,
                depends_on=[],
            )
            for index, question in enumerate(
                questions,
                start=1,
            )
        ]