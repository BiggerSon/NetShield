from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class SecurityEvent:
    timestamp: str
    event_type: str
    severity: str
    risk_score: int

    source: Optional[str] = None
    destination: Optional[str] = None

    message: str = ""
    details: dict = None

    def to_dict(self):
        data = asdict(self)

        if data["details"] is None:
            data["details"] = {}

        return data


def create_event(
    event_type,
    severity,
    risk_score,
    source=None,
    destination=None,
    message="",
    details=None
):
    return SecurityEvent(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        event_type=event_type,
        severity=severity,
        risk_score=max(0, min(100, int(risk_score))),
        source=source,
        destination=destination,
        message=message,
        details=details or {}
    )