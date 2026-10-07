
from src.rag.pipeline import ParentChildRAG
from src.rag.multivector_pipeline import MultiVectorRAG
from src.rag.query_rewriter import QueryRewriter


class UnifiedRAG:

    def __init__(self):

        self.parent_child = None
        self.multivector = None

        self.query_rewriter = QueryRewriter()

    def _get_parent_child(self):

        if self.parent_child is None:
            self.parent_child = ParentChildRAG()

        return self.parent_child

    def _get_multivector(self):

        if self.multivector is None:
            self.multivector = MultiVectorRAG()

        return self.multivector

    def _rewrite_query(
        self,
        query,
        history=None,
    ):

        return self.query_rewriter.rewrite(
            query,
            history,
        )

    def ask(
        self,
        query,
        mode="multivector",
        expand=True,
        history=None,
    ):

        standalone_query = self._rewrite_query(
            query,
            history,
        )

        if mode == "parent_child":

            rag = self._get_parent_child()

            result = rag.ask(
                standalone_query
            )

            result["original_query"] = query
            result["query"] = standalone_query
            result["mode"] = "parent_child"

            return result

        if mode == "multivector":

            rag = self._get_multivector()

            result = rag.ask(
                standalone_query,
                expand=expand,
            )

            result["original_query"] = query
            result["query"] = standalone_query
            result["mode"] = "multivector"

            return result

        raise ValueError(
            f"Unknown retrieval mode: {mode}"
        )
