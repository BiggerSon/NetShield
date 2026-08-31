from app.state import STATE


SEVERITY_POINTS = {
    "LOW": 15,
    "MEDIUM": 30,
    "HIGH": 50,
    "CRITICAL": 75
}


def calculate_score(event_type, severity, source):
    points = SEVERITY_POINTS.get(severity, 10)
    with STATE.lock:
        old_score = STATE.risk_scores.get(source, 0)
        new_score = min(
            100,
            old_score + points
        )
        STATE.risk_scores[source] = new_score
    return new_score


def severity_from_score(score):
    if score >= 90:
        return "CRITICAL"
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"


def decay_risk_scores():
    with STATE.lock:
        for ip in list(STATE.risk_scores):
            STATE.risk_scores[ip] = max(
                0,
                STATE.risk_scores[ip] - 1
            )