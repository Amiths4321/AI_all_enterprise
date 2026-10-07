from enum import Enum


class QueryRelationship(str, Enum):
    INDEPENDENT = "independent"
    DEPENDENT = "dependent"
    COMPARISON = "comparison"