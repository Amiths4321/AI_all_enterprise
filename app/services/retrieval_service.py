from app.core.security import AccessPolicy, UserContext
from app.retrieval.query_analyzer import QueryAnalyzer
from app.retrieval.intent import IntentClassifier
from app.retrieval.strategy import RetrievalStrategySelector
from app.retrieval.diagnostics import RetrievalDiagnostics
from app.retrieval.confidence import RetrievalConfidenceEvaluator
from app.core.timing import StageTimer


class EnterpriseRetrievalService:

    def __init__(
        self,
        retriever,
        reranker,
        access_policy: AccessPolicy,
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.access_policy = access_policy

        self.query_analyzer = QueryAnalyzer()
        self.intent_classifier = IntentClassifier()
        self.strategy_selector = RetrievalStrategySelector()
        self.confidence_evaluator = RetrievalConfidenceEvaluator()

    def retrieve(
        self,
        question: str,
        user: UserContext,
        top_k: int = 10,
        top_n: int = 3,
    ):

        analysis = self.query_analyzer.analyze(question)

        intent = self.intent_classifier.classify(
            analysis.normalized_question
        )

        strategy = self.strategy_selector.select(intent)

        timer = StageTimer()

        with timer.measure("query_analysis"):
            analysis = self.query_analyzer.analyze(
                question
            )

        with timer.measure("intent"):
            intent = self.intent_classifier.classify(
                analysis.normalized_question
            )

        with timer.measure("retrieval"):
            retrieved = self.retriever.retrieve(
                question,
                top_k=top_k,
                filters=filters,
                strategy=strategy.value,
            )

        with timer.measure("authorization"):
            authorized = [
                document
                for document in retrieved
                if self.access_policy.can_access(
                    user,
                    document,
                )
            ]

        with timer.measure("reranking"):
            reranked = self.reranker.rerank(
                question,
                authorized,
                top_n=top_n,
            )
        filters = {}

        if analysis.department:
            filters["department"] = analysis.department

        if analysis.document_type:
            filters["document_type"] = analysis.document_type

        if analysis.year:
            filters["year"] = analysis.year

        filters["access_level"] = (
            self.access_policy.allowed_levels(user)
        )

        if user.department:
            filters["department"] = user.department

        retrieved = self.retriever.retrieve(
            question,
            top_k=top_k,
            filters=filters,
            strategy=strategy.value,
        )

        authorized = [
            document
            for document in retrieved
            if self.access_policy.can_access(
                user,
                document,
            )
        ]

        reranked = self.reranker.rerank(
            question,
            authorized,
            top_n=top_n,
        )

        confidence = self.confidence_evaluator.evaluate(
            reranked
        )

        diagnostics = RetrievalDiagnostics().analyze(
            retrieved,
            reranked,
        )

        return {
            "analysis": analysis,
            "intent": intent,
            "strategy": strategy,
            "filters": filters,
            "retrieved": authorized,
            "reranked": reranked,
            "confidence": confidence,
            "diagnostics": diagnostics,
            "timing": {
            "stages": timer.result.stages,
            "total_ms": timer.result.total_ms,
        },
        }