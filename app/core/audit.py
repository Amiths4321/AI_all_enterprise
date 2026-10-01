from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class SecurityEvent:
    event_type: str
    user_id: str
    question: str
    document_id: str | None
    allowed: bool
    timestamp: str


class SecurityAuditor:

    def record(
        self,
        event_type: str,
        user_id: str,
        question: str,
        document_id: str | None,
        allowed: bool,
    ) -> SecurityEvent:

        return SecurityEvent(
            event_type=event_type,
            user_id=user_id,
            question=question,
            document_id=document_id,
            allowed=allowed,
            timestamp=datetime.now(
                timezone.utc
            ).isoformat(),
        )